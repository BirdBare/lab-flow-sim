import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager

from orm.workcell.models import Workcell
from orm.workcell_process.models import BaseStep, Process, StepIndex, Swimlane, SwimlaneIndex
from webapp.tabs import workcell_process_metadata, workcell_process_swimlanes

_KEY_PREFIX = "workcell_processes"


#
# IS_EDITABLE
#
def get_is_editable_key() -> str:
    return f"{_KEY_PREFIX}_is_editable"


def set_is_editable(value: bool):
    streamlit.session_state[get_is_editable_key()] = value


def get_is_editable() -> bool:
    return streamlit.session_state.get(get_is_editable_key(), False)


#
# FORCE UPDATE
#
def get_force_update_key() -> str:
    return f"{_KEY_PREFIX}_force_update"


def get_force_update() -> bool:
    return streamlit.session_state.get(get_force_update_key(), False)


def set_force_update(value: bool):
    streamlit.session_state[get_force_update_key()] = value


#
# Processes
#
def get_processes_key() -> str:
    return f"{_KEY_PREFIX}_processes"


def get_processes() -> list[Process]:
    if get_processes_key() not in streamlit.session_state:
        reset_processes()

    return streamlit.session_state[get_processes_key()]


def reset_processes():
    streamlit.session_state[get_processes_key()] = []


#
# SELECTBOX_PROCESS
#
def get_selectbox_process_key() -> str:
    return f"{_KEY_PREFIX}_selectbox_process"


def set_selectbox_process(value: Process):
    streamlit.session_state[get_selectbox_process_key()] = value


def get_selectbox_process() -> Process:
    return streamlit.session_state.get(get_selectbox_process_key(), False)


#
# BUTTON CALLBACKS
#
def callback_button_new_process(workcell=Workcell):
    process = Process(workcell=workcell, name="New Process - RENAME ME", comments="")

    get_processes().append(process)
    set_selectbox_process(process)

    set_is_editable(True)
    set_force_update(True)


def callback_button_delete_process(process: Process):
    process.delete()


def callback_button_enable_edits():
    set_is_editable(True)


def callback_button_discard_edits():
    set_is_editable(False)


def callback_button_save_edits(process: Process):
    process.save()

    for swimlane in Swimlane.objects.filter(process=process).all():
        if swimlane not in workcell_process_swimlanes.get_swimlanes():
            swimlane.delete()

    for swimlane_index, swimlane in enumerate(workcell_process_swimlanes.get_swimlanes()):
        swimlane.save()

        SwimlaneIndex.objects.filter(swimlane=swimlane).delete()

        SwimlaneIndex(swimlane=swimlane, index=swimlane_index).save()

    for swimlane, steps in workcell_process_swimlanes.get_swimlane_steps_dict().items():
        # I can delete all the previous steps in the swimlane and rebuild. Is faster and easier to read.
        BaseStep.objects.filter(swimlane=swimlane).delete()

        for step_index, step in enumerate(steps):
            step.save()

            StepIndex(base_step=step, index=step_index).save()

    set_is_editable(False)


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(get_is_editable_key())

    session_state_manager.add_persistent_keys(get_processes_key())
    if not get_is_editable():
        reset_processes()
        for process in Process.objects.filter(workcell=workcell).order_by(Lower("name")).all():
            get_processes().append(process)

    with streamlit.container(horizontal=True, vertical_alignment="bottom"):
        session_state_manager.add_persistent_keys("selectbox_process")
        process = streamlit.selectbox(
            "Select A Process",
            get_processes(),
            key=get_selectbox_process_key(),
            disabled=get_is_editable(),
            format_func=lambda x: x.name,
            width=600,
        )

        if not get_is_editable():
            streamlit.button(
                "New Process",
                width=130,
                key=f"button_{_KEY_PREFIX}_new_process",
                on_click=callback_button_new_process,
                args=(workcell,),
            )

        if process is None:
            streamlit.stop()

        if get_is_editable():
            streamlit.button(
                "Discard Edits",
                width=130,
                key=f"button_{_KEY_PREFIX}_enable_edits",
                on_click=callback_button_discard_edits,
            )
            streamlit.button(
                "Save Edits",
                width=130,
                key=f"button_{_KEY_PREFIX}_delete_process",
                on_click=callback_button_save_edits,
                args=(process,),
            )
        else:
            streamlit.button(
                "Enable Edits",
                width=130,
                key=f"button_{_KEY_PREFIX}_enable_edits",
                on_click=callback_button_enable_edits,
            )
            streamlit.button(
                "Delete Process",
                width=130,
                key=f"button_{_KEY_PREFIX}_delete_process",
                on_click=callback_button_delete_process,
                args=(process,),
            )

    if get_is_editable():
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
        workcell_process_metadata.render_tab(session_state_manager, process, get_is_editable(), get_force_update())

    with workcell_process_swimlanes_tab:
        workcell_process_swimlanes.render_tab(session_state_manager, process, get_is_editable(), get_force_update())

    if workcell_process_diagram_tab is not None:
        with workcell_process_diagram_tab:
            ...

    set_force_update(False)
