import datetime

import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager

import webapp.state.workcell_processes_tab_state as state
from orm.workcell.models import Workcell
from orm.workcell_process.models import BaseStep, Process, StepIndex, Swimlane, SwimlaneIndex
from webapp.state import workcell_process_swimlanes_tab_state
from webapp.tabs import workcell_process_metadata_tab, workcell_process_swimlanes_tab


#
# BUTTON CALLBACKS
#
def callback_button_new_process(workcell=Workcell):
    process = Process(
        workcell=workcell,
        name=f"RENAME ME - New Process - {datetime.datetime.now().strftime('%d%m%Y:%H%M%S|%f')}",
        comments="",
    )

    state.Processes.get().append(process)
    state.SelectboxProcess.set(process)

    state.IsEditable.set(True)
    state.ForceUpdate.set(True)


def callback_button_delete_process(process: Process):
    process.delete()


def callback_button_enable_edits():
    state.IsEditable.set(True)


def callback_button_discard_edits():
    state.IsEditable.set(False)


def callback_button_save_edits(process: Process):
    process.save()

    state.SelectboxProcess.set(process)

    for swimlane in Swimlane.objects.filter(process=process).all():
        if swimlane not in workcell_process_swimlanes_tab_state.Swimlanes.get():
            swimlane.delete()

    for swimlane_index, swimlane in enumerate(workcell_process_swimlanes_tab_state.Swimlanes.get()):
        swimlane.save()

        SwimlaneIndex.objects.filter(swimlane=swimlane).delete()

        SwimlaneIndex(swimlane=swimlane, index=swimlane_index).save()

    for swimlane, steps in workcell_process_swimlanes_tab_state.SwimlaneStepsBySwimlane.get().items():
        # I can delete all the previous steps in the swimlane and rebuild. Is faster and easier to read.
        BaseStep.objects.filter(swimlane=swimlane).delete()

        for step_index, step in enumerate(steps):
            step.save()

            StepIndex(base_step=step, index=step_index).save()

    state.IsEditable.set(False)


#
# TAB
#
def render(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(state.IsEditable.key(), state.ForceUpdate.key())

    session_state_manager.add_persistent_keys(state.Processes.key())
    if not state.IsEditable.get():
        # Reset the state
        state.Processes.set([])

        for process in Process.objects.filter(workcell=workcell).order_by(Lower("name")).all():
            state.Processes.get().append(process)

    with streamlit.container(horizontal=True, vertical_alignment="bottom"):
        session_state_manager.add_persistent_keys(state.SelectboxProcess.key())
        process = streamlit.selectbox(
            "Select A Process",
            state.Processes.get(),
            key=state.SelectboxProcess.key(),
            disabled=state.IsEditable.get(),
            format_func=lambda x: x.name,
            width=600,
        )

        if not state.IsEditable.get():
            streamlit.button(
                "New Process",
                width=130,
                key=f"{state.KEY_PREFIX}_button_new_process",
                on_click=callback_button_new_process,
                args=(workcell,),
            )

        if process is None:
            streamlit.stop()

        if state.IsEditable.get():
            streamlit.button(
                "Discard Edits",
                width=130,
                key=f"{state.KEY_PREFIX}_button_enable_edits",
                on_click=callback_button_discard_edits,
            )
            streamlit.button(
                "Save Edits",
                width=130,
                key=f"{state.KEY_PREFIX}_button_delete_process",
                on_click=callback_button_save_edits,
                args=(process,),
            )
        else:
            streamlit.button(
                "Enable Edits",
                width=130,
                key=f"{state.KEY_PREFIX}_button_enable_edits",
                on_click=callback_button_enable_edits,
            )
            streamlit.button(
                "Delete Process",
                width=130,
                key=f"{state.KEY_PREFIX}_button_delete_process",
                on_click=callback_button_delete_process,
                args=(process,),
            )

    if state.IsEditable.get():
        (workcell_process_metadata, workcell_process_swimlanes), workcell_process_diagram = (
            streamlit.tabs(
                ["Process Metadata", "Process Swimlanes"],
            ),
            None,
        )
    else:
        workcell_process_metadata, workcell_process_swimlanes, workcell_process_diagram = streamlit.tabs(
            ["Process Metadata", "Process Swimlanes", "Process Diagram"],
        )

    with workcell_process_metadata:
        workcell_process_metadata_tab.render(
            session_state_manager,
            process,
            state.IsEditable.get(),
            state.ForceUpdate.get(),
        )

    with workcell_process_swimlanes:
        workcell_process_swimlanes_tab.render(
            session_state_manager,
            process,
            state.IsEditable.get(),
            state.ForceUpdate.get(),
        )

    if workcell_process_diagram is not None:
        with workcell_process_diagram:
            ...

    state.ForceUpdate.set(False)
