import datetime

import streamlit
from utils import SessionStateManager, webapp_menu

import webapp.state.workcells_page_state as state
from orm.workcell.models import Workcell
from webapp.state import workcell_layout_tab_state, workcell_metadata_tab_state, workcell_processes_tab_state
from webapp.tabs import workcell_labware_tab, workcell_layout_tab, workcell_metadata_tab, workcell_processes_tab


#
# CALLBACKS
#
def callback_button_new_workcell():
    workcell = Workcell(
        name=f"RENAME ME - New Process - {datetime.datetime.now().strftime('%d%m%Y:%H%M%S|%f')}",
        comments="",
    )
    workcell.save()
    state.SelectboxWorkcell.set(workcell)


def callback_button_delete_workcell(workcell: Workcell):
    workcell.delete()


streamlit.set_page_config(page_title="Workcells", layout="wide")

webapp_menu()

with SessionStateManager() as session_state_manager:
    streamlit.title("Workcells")

    streamlit.text(
        "Workcells can be created here. Once a workcell is created with its associated devices you can create processes.",
    )

    # Render selectbox
    session_state_manager.add_persistent_keys(state.SelectboxWorkcell.key())
    workcell = streamlit.selectbox(
        "Select A Workcell",
        sorted(
            Workcell.objects.all(),
            key=lambda x: x.name,
        ),
        key=state.SelectboxWorkcell.key(),
        disabled=workcell_metadata_tab_state.IsEditable.get()
        or workcell_layout_tab_state.IsEditable.get()
        or workcell_processes_tab_state.IsEditable.get(),
        format_func=lambda x: x.name,
        width=800,
    )

    with streamlit.container(horizontal=True):
        streamlit.button(
            "New Workcell",
            width=150,
            on_click=callback_button_new_workcell,
            disabled=workcell_metadata_tab_state.IsEditable.get()
            or workcell_layout_tab_state.IsEditable.get()
            or workcell_processes_tab_state.IsEditable.get(),
        )

        if workcell is None:
            streamlit.stop()

        streamlit.button(
            "Delete Workcell",
            width=150,
            on_click=callback_button_delete_workcell,
            args=(workcell,),
            disabled=workcell_metadata_tab_state.IsEditable.get()
            or workcell_layout_tab_state.IsEditable.get()
            or workcell_processes_tab_state.IsEditable.get(),
        )

    streamlit.session_state["workcell_error_container"] = streamlit.container()

    workcell_metadata, workcell_diagram, workcell_labware, workcell_processes = streamlit.tabs(
        ["Workcell Metadata", "Workcell Layout", "Workcell Labware", "Workcell Processes"],
    )

    with workcell_labware:
        workcell_labware_tab.render_tab(session_state_manager, workcell)

    with workcell_metadata:
        workcell_metadata_tab.render_tab(session_state_manager, workcell)

    with workcell_diagram:
        workcell_layout_tab.render_tab(session_state_manager, workcell)

    with workcell_processes:
        workcell_processes_tab.render_tab(session_state_manager, workcell)
