import datetime

import streamlit
from utils import SessionStateManager, webapp_menu

from orm.workcell.models import Workcell
from webapp.tabs import workcell_labware, workcell_layout, workcell_metadata, workcell_processes


#
# WORKCELL SELECTBOX
#
def get_workcell_selectbox_key() -> str:
    return "selectbox_workcell"


def get_selectbox_workcell() -> Workcell:
    return streamlit.session_state[get_workcell_selectbox_key()]


def set_selectbox_workcell(workcell: Workcell):
    streamlit.session_state[get_workcell_selectbox_key()] = workcell


#
# CALLBACKS
#
def callback_button_new_workcell():
    workcell = Workcell(
        name=f"RENAME ME - New Process - {datetime.datetime.now().strftime('%d%m%Y:%H%M%S|%f')}",
        comments="",
    )
    workcell.save()
    set_selectbox_workcell(workcell)


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
    session_state_manager.add_persistent_keys("selectbox_workcell")
    workcell = streamlit.selectbox(
        "Select A Workcell",
        sorted(
            Workcell.objects.all(),
            key=lambda x: x.name,
        ),
        key=get_workcell_selectbox_key(),
        disabled=workcell_metadata.get_is_editable()
        or workcell_layout.get_is_editable()
        or workcell_processes.get_is_editable(),
        format_func=lambda x: x.name,
        width=800,
    )

    with streamlit.container(horizontal=True):
        streamlit.button(
            "New Workcell",
            width=150,
            on_click=callback_button_new_workcell,
            disabled=workcell_metadata.get_is_editable()
            or workcell_layout.get_is_editable()
            or workcell_processes.get_is_editable(),
        )

        if workcell is None:
            streamlit.stop()

        streamlit.button(
            "Delete Workcell",
            width=150,
            on_click=callback_button_delete_workcell,
            args=(workcell,),
            disabled=workcell_metadata.get_is_editable()
            or workcell_layout.get_is_editable()
            or workcell_processes.get_is_editable(),
        )

    streamlit.session_state["workcell_error_container"] = streamlit.container()

    workcell_metadata_tab, workcell_diagram_tab, workcell_labware_tab, workcell_processes_tab = streamlit.tabs(
        ["Workcell Metadata", "Workcell Layout", "Workcell Labware", "Workcell Processes"],
    )

    with workcell_labware_tab:
        workcell_labware.render_tab(session_state_manager, workcell)

    with workcell_metadata_tab:
        workcell_metadata.render_tab(session_state_manager, workcell)

    with workcell_diagram_tab:
        workcell_layout.render_tab(session_state_manager, workcell)

    with workcell_processes_tab:
        workcell_processes.render_tab(session_state_manager, workcell)
