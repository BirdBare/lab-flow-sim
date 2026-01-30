import streamlit
from utils import SessionStateManager

from django_orm.process.models import (
    BaseStep,
    FunctionStep,
    Process,
    ProcessStep,
    StepIndex,
    Swimlane,
    SwimlaneIndex,
)


def render_process_builder_tab(session_state_manager: SessionStateManager, process_is_editable: bool, process: Process):
    if process_is_editable is True:
        with streamlit.container(horizontal_alignment="center"):
            streamlit.button("Add Swimlane", on_click=Swimlane.streamlit_callback_button_add_swimlane)

    session_state_manager.add_persistent_keys("process_swimlanes")

    if process_is_editable is False:
        streamlit.session_state["process_swimlanes"] = [
            swimlane_index.swimlane
            for swimlane_index in SwimlaneIndex.objects.filter(
                swimlane__process=process,
            )
            .order_by("index")
            .all()
        ]

    process_swimlanes: list[Swimlane] = streamlit.session_state["process_swimlanes"]

    process_swimlane_chunks = [process_swimlanes[i : i + 3] for i in range(0, len(process_swimlanes), 3)]

    tabs = streamlit.tabs([f"Page {i + 1}" for i in range(max(len(process_swimlane_chunks), 1))])

    for chunk_index, process_swimlane_chunk in enumerate(process_swimlane_chunks):
        with tabs[chunk_index], streamlit.container(horizontal=True, horizontal_alignment="center"):
            columns = streamlit.columns(3)
            for swimlane_index, process_swimlane in enumerate(process_swimlane_chunk):
                with columns[swimlane_index], streamlit.container(border=True, gap=None):
                    process_swimlane.streamlit_render_fields(
                        session_state_manager,
                        process_is_editable,
                        chunk_index * 3 + swimlane_index,
                    )

                    streamlit.divider()

                    if process_is_editable is True:
                        with streamlit.container(horizontal_alignment="center", horizontal=True):
                            FunctionStep.streamlit_render_add_button(process_swimlane, "before", 0)
                            ProcessStep.streamlit_render_add_button(process_swimlane, "before", 0)

                    session_state_manager.add_persistent_keys(f"process_swimlane_{process_swimlane.id}_steps")
                    if process_is_editable is False:
                        streamlit.session_state[f"process_swimlane_{process_swimlane.id}_steps"] = [
                            step_index.base_step.cast()
                            for step_index in StepIndex.objects.filter(base_step__swimlane=process_swimlane)
                            .order_by("index")
                            .all()
                        ]
                    process_swimlane_steps: list[BaseStep] = streamlit.session_state[
                        f"process_swimlane_{process_swimlane.id}_steps"
                    ]

                    for step_index, process_swimlane_step in enumerate(
                        process_swimlane_steps,
                    ):
                        with streamlit.container(border=True, gap=None):
                            process_swimlane_step.streamlit_render_fields(
                                session_state_manager,
                                process_is_editable,
                                step_index,
                            )

                        if process_is_editable is True:
                            with streamlit.container(horizontal_alignment="center", horizontal=True):
                                FunctionStep.streamlit_render_add_button(
                                    process_swimlane,
                                    f"after_{process_swimlane_step.id}",
                                    step_index + 1,
                                )
                                ProcessStep.streamlit_render_add_button(
                                    process_swimlane,
                                    f"after_{process_swimlane_step.id}",
                                    step_index + 1,
                                )
                        else:
                            streamlit.markdown("<br>", unsafe_allow_html=True)
