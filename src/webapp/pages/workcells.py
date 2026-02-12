import streamlit
from utils import SessionStateManager, webapp_menu

from orm.workcell.models import Workcell
from webapp.tabs import workcell_diagram, workcell_labware, workcell_metadata


#
# WORKCELL SELECTBOX
#
def get_workcell_selectbox_key() -> str:
    return "selectbox_workcell"


def get_selectbox_workcell() -> Workcell:
    return streamlit.session_state[get_workcell_selectbox_key()]


def set_selectbox_workcell(workcell: Workcell):
    streamlit.session_state[get_workcell_selectbox_key()] = workcell


def selectbox_workcell_on_change():
    workcell_metadata.set_is_editable(False)
    workcell_diagram.set_is_editable(False)
    workcell_diagram.reset_streamlit_flow_state(get_selectbox_workcell())


streamlit.set_page_config(page_title="Workcells", layout="wide")

webapp_menu()

with SessionStateManager() as session_state_manager:
    streamlit.title("Workcells")

    streamlit.text(
        "Workcells can be created here. Once a workcell is created with its associated devices you can create processes.",
    )

    # Render selectbox
    session_state_manager.add_persistent_keys("selectbox_workcell")
    workcell = streamlit.selectbox(
        "Select A Workcell",
        sorted(
            Workcell.objects.all(),
            key=lambda x: x.name,
        ),
        key=get_workcell_selectbox_key(),
        disabled=False,  # TODO
        format_func=lambda x: x.name,
        width=800,
        on_change=selectbox_workcell_on_change,
    )

    streamlit.button("New Workcell", width=150, on_click=lambda: None)

    if workcell is None:
        streamlit.stop()

    streamlit.session_state["workcell_error_container"] = streamlit.container()

    workcell_metadata_tab, workcell_diagram_tab, workcell_labware_tab, workcell_processes_tab = streamlit.tabs(
        ["Workcell Metadata", "Workcell Diagram", "Workcell Labware", "Workcell Processes"],
    )

    with workcell_labware_tab:
        workcell_labware.render_tab(session_state_manager, workcell)

    with workcell_metadata_tab:
        workcell_metadata.render_tab(session_state_manager, workcell)

    with workcell_diagram_tab:
        workcell_diagram.render_tab(session_state_manager, workcell)

    with workcell_processes_tab:
        ...
