import streamlit
from tabs.workcell_diagram_tab import render_workcell_diagram_tab, reset_workcell_streamlit_flow_state
from utils import SessionStateManager, webapp_menu

from orm.workcell.models import Workcell


def selectbox_workcell_on_change():
    streamlit.session_state["workcell_is_editable"] = False
    reset_workcell_streamlit_flow_state(streamlit.session_state["selectbox_workcell"])


streamlit.set_page_config(page_title="Workcells", layout="wide")

webapp_menu()

with SessionStateManager() as session_state_manager:
    streamlit.title("Workcells")

    streamlit.text(
        "Workcells can be created here. Once a workcell is created with its associated devices you can create processes.",
    )

    session_state_manager.add_persistent_keys("workcell_is_editable")
    workcell_is_editable = streamlit.session_state.get("workcell_is_editable", False)

    # Render selectbox
    session_state_manager.add_persistent_keys("selectbox_workcell")
    workcell = streamlit.selectbox(
        "Select A Workcell",
        sorted(
            Workcell.objects.all(),
            key=lambda x: x.name,
        ),
        key="selectbox_workcell",
        disabled=workcell_is_editable,
        format_func=lambda x: x.name,
        width=800,
        on_change=selectbox_workcell_on_change,
    )

    with streamlit.container(horizontal=True):
        if workcell_is_editable is False:
            streamlit.button("New Workcell", width=150, on_click=lambda: None)
            if workcell is not None:

                def fun():
                    streamlit.session_state["workcell_is_editable"] = True

                streamlit.button("Edit Workcell", width=150, on_click=fun)
        else:
            streamlit.button("Save Workcell", width=150, on_click=lambda: None)

            def fun():
                streamlit.session_state["workcell_is_editable"] = False

            streamlit.button("Cancel Edits", width=150, on_click=fun)
            if workcell.name != "New Workcell":
                streamlit.button("Delete Workcell", width=150, on_click=lambda: None)

    if workcell is None:
        streamlit.stop()

    streamlit.session_state["workcell_error_container"] = streamlit.container()

    session_state_manager.add_persistent_keys("text_input_workcell_name")

    with streamlit.container(horizontal_alignment="center"):
        if workcell_is_editable:
            streamlit.text_input(
                "Updated Workcell Name",
                width=800,
                disabled=not workcell_is_editable,
                key="text_input_workcell_name",
                value=workcell.name,
            )

    workcell_diagram_tab, workcell_processes_tab = streamlit.tabs(["Workcell Diagram", "Workcell Processes"])

    with workcell_diagram_tab:
        render_workcell_diagram_tab(session_state_manager, workcell_is_editable, workcell)
