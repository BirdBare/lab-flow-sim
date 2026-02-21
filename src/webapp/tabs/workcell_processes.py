import datetime

import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager

import webapp.state.workcell_processes_tab_state as state
from orm.workcell.models import Workcell
from orm.workcell_process.models import BaseStep, Process, StepIndex, Swimlane, SwimlaneIndex
from webapp.state import workcell_process_swimlanes_tab_state
from webapp.tabs import workcell_process_metadata, workcell_process_swimlanes


#
# BUTTON CALLBACKS
#
def callback_button_new_process(workcell=Workcell):
    process = Process(
        workcell=workcell,
        name=f"RENAME ME - New Process - {datetime.datetime.now().strftime('%d%m%Y:%H%M%S|%f')}",
        comments="",
    )

    state.get_processes().append(process)
    state.set_selectbox_process(process)

    state.set_is_editable(True)
    state.set_force_update(True)


def callback_button_delete_process(process: Process):
    process.delete()


def callback_button_enable_edits():
    state.set_is_editable(True)


def callback_button_discard_edits():
    state.set_is_editable(False)


def callback_button_save_edits(process: Process):
    process.save()

    state.set_selectbox_process(process)

    for swimlane in Swimlane.objects.filter(process=process).all():
        if swimlane not in workcell_process_swimlanes_tab_state.get_swimlanes():
            swimlane.delete()

    for swimlane_index, swimlane in enumerate(workcell_process_swimlanes_tab_state.get_swimlanes()):
        swimlane.save()

        SwimlaneIndex.objects.filter(swimlane=swimlane).delete()

        SwimlaneIndex(swimlane=swimlane, index=swimlane_index).save()

    for swimlane, steps in workcell_process_swimlanes_tab_state.get_swimlane_steps_dict().items():
        # I can delete all the previous steps in the swimlane and rebuild. Is faster and easier to read.
        BaseStep.objects.filter(swimlane=swimlane).delete()

        for step_index, step in enumerate(steps):
            step.save()

            StepIndex(base_step=step, index=step_index).save()

    state.set_is_editable(False)


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(state.get_is_editable_key())

    session_state_manager.add_persistent_keys(state.get_processes_key())
    if not state.get_is_editable():
        state.reset_processes()
        for process in Process.objects.filter(workcell=workcell).order_by(Lower("name")).all():
            state.get_processes().append(process)

    with streamlit.container(horizontal=True, vertical_alignment="bottom"):
        session_state_manager.add_persistent_keys("selectbox_process")
        process = streamlit.selectbox(
            "Select A Process",
            state.get_processes(),
            key=state.get_selectbox_process_key(),
            disabled=state.get_is_editable(),
            format_func=lambda x: x.name,
            width=600,
        )

        if not state.get_is_editable():
            streamlit.button(
                "New Process",
                width=130,
                key=f"button_{state._KEY_PREFIX}_new_process",
                on_click=callback_button_new_process,
                args=(workcell,),
            )

        if process is None:
            streamlit.stop()

        if state.get_is_editable():
            streamlit.button(
                "Discard Edits",
                width=130,
                key=f"button_{state._KEY_PREFIX}_enable_edits",
                on_click=callback_button_discard_edits,
            )
            streamlit.button(
                "Save Edits",
                width=130,
                key=f"button_{state._KEY_PREFIX}_delete_process",
                on_click=callback_button_save_edits,
                args=(process,),
            )
        else:
            streamlit.button(
                "Enable Edits",
                width=130,
                key=f"button_{state._KEY_PREFIX}_enable_edits",
                on_click=callback_button_enable_edits,
            )
            streamlit.button(
                "Delete Process",
                width=130,
                key=f"button_{state._KEY_PREFIX}_delete_process",
                on_click=callback_button_delete_process,
                args=(process,),
            )

    if state.get_is_editable():
        (workcell_process_metadata_tab, workcell_process_swimlanes_tab), workcell_process_diagram_tab = (
            streamlit.tabs(
                ["Process Metadata", "Process Swimlanes"],
            ),
            None,
        )
    else:
        workcell_process_metadata_tab, workcell_process_swimlanes_tab, workcell_process_diagram_tab = streamlit.tabs(
            ["Process Metadata", "Process Swimlanes", "Process Diagram"],
        )

    with workcell_process_metadata_tab:
        workcell_process_metadata.render_tab(
            session_state_manager, process, state.get_is_editable(), state.get_force_update()
        )

    with workcell_process_swimlanes_tab:
        workcell_process_swimlanes.render_tab(
            session_state_manager, process, state.get_is_editable(), state.get_force_update()
        )

    if workcell_process_diagram_tab is not None:
        with workcell_process_diagram_tab:
            ...

    state.set_force_update(False)
