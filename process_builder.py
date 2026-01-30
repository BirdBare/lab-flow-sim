import streamlit
from tabs import (
    render_process_builder_tab,
    render_process_graph_tab,
)
from utils import SessionStateManager, webapp_menu

from django_orm.process.models import (
    BaseStep,
    Process,
    StepIndex,
    Swimlane,
    SwimlaneIndex,
)

streamlit.set_page_config(page_title="Process Builder", layout="wide")


webapp_menu()


def callback_button_add_process():
    new_process = Process(name="New Process")
    new_process.save()

    streamlit.session_state["selectbox_process"] = new_process
    streamlit.session_state["process_swimlanes"] = []

    streamlit.session_state["process_is_editable"] = True


def callback_button_edit_process():
    streamlit.session_state["process_is_editable"] = True


def callback_button_cancel_process():
    process: Process = streamlit.session_state["selectbox_process"]
    if process.name == "New Process":
        process.delete()

    streamlit.session_state["process_is_editable"] = False


def callback_button_delete_process():
    selected_process: Process = streamlit.session_state["selectbox_process"]
    selected_process.delete()

    streamlit.session_state["process_is_editable"] = False


def callback_button_save_process():
    process: Process = streamlit.session_state["selectbox_process"]

    if streamlit.session_state["text_input_process_name"] == "New Process":
        with streamlit.session_state["error_container"]:
            streamlit.error("Please change the process name. Process cannot be named 'New Process.'")
        return

    # We will rebuild from scratch. Just easier in my mind.
    process.name = streamlit.session_state["text_input_process_name"]
    process.save()

    SwimlaneIndex.objects.filter(swimlane__process=process).delete()
    StepIndex.objects.filter(base_step__swimlane__process=process).delete()
    for swimlane in Swimlane.objects.filter(process=process).all():
        BaseStep.objects.filter(swimlane=swimlane).delete()
        if swimlane not in streamlit.session_state["process_swimlanes"]:
            swimlane.delete()

    process_swimlanes: list[Swimlane] = streamlit.session_state["process_swimlanes"]
    for swimlane_index, process_swimlane in enumerate(process_swimlanes):
        process_swimlane.streamlit_update_fields()
        process_swimlane.clean()
        process_swimlane.save()
        SwimlaneIndex(swimlane=process_swimlane, index=swimlane_index).save()

        process_swimlane_steps: list[BaseStep] = streamlit.session_state[
            f"process_swimlane_{process_swimlane.id}_steps"
        ]
        for step_index, process_swimlane_step in enumerate(process_swimlane_steps):
            process_swimlane_step.streamlit_update_fields()
            process_swimlane_step.clean()
            process_swimlane_step.save()
            StepIndex(base_step=process_swimlane_step, index=step_index).save()

    streamlit.session_state["selectbox_process"] = process

    streamlit.session_state["process_is_editable"] = False


with SessionStateManager(
    "process_is_editable",
    "selectbox_process_extra_items",
    "error_container",
) as session_state_manager:
    process_is_editable = streamlit.session_state.get("process_is_editable", False)

    streamlit.title("Process Builder")
    with streamlit.container(width=800):
        streamlit.text(
            "Processes will be built here using functions defined in the 'Device Functions' table. Processes can also reference other processes. A process will be comprised of a number of swim lanes each containing 1 or more steps.",
        )

        session_state_manager.add_persistent_keys("selectbox_process")

        # Render selectbox
        process = streamlit.selectbox(
            "Select A Process",
            sorted(
                Process.objects.all(),
                key=lambda x: x.name,
            ),
            key="selectbox_process",
            disabled=process_is_editable,
            format_func=lambda x: x.name,
        )

        with streamlit.container(horizontal=True):
            if process_is_editable is False:
                streamlit.button("New Process", width=125, on_click=callback_button_add_process)
                if process is not None:
                    streamlit.button("Edit Process", width=125, on_click=callback_button_edit_process)
            else:
                streamlit.button("Save Process", width=125, on_click=callback_button_save_process)
                streamlit.button("Cancel Edits", width=125, on_click=callback_button_cancel_process)
                if process.name != "New Process":
                    streamlit.button("Delete Process", width=125, on_click=callback_button_delete_process)

    if process is None:
        streamlit.stop()

    streamlit.session_state["error_container"] = streamlit.container()

    session_state_manager.add_persistent_keys("text_input_process_name")
    if process_is_editable is True:
        streamlit.markdown("<br>", unsafe_allow_html=True)
        with streamlit.container(horizontal_alignment="center"):
            streamlit.text_input(
                "Process Name",
                width=800,
                label_visibility="collapsed",
                value=process.name,
                key="text_input_process_name",
            )

    process_tab, process_graph_tab = streamlit.tabs(
        ["Process", "Process Graph"],
    )

    with process_tab:
        render_process_builder_tab(session_state_manager, process_is_editable, process)

    with process_graph_tab:
        render_process_graph_tab(session_state_manager, process_is_editable, process)
