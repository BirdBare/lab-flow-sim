import streamlit
from utils import SessionStateManager

from orm.workcell_process.models import Process

_KEY_PREFIX = "workcell_process_metadata"


#
# PROCESS NAME
#
def get_text_input_process_name_key() -> str:
    return f"{_KEY_PREFIX}_text_input_process_name"


def set_text_input_process_name(value: str):
    streamlit.session_state[get_text_input_process_name_key()] = value


#
# PROCESS COMMENTS
#
def get_text_area_process_comments_key() -> str:
    return f"{_KEY_PREFIX}_text_area_process_comments"


def set_text_area_process_comments(value: str):
    streamlit.session_state[get_text_area_process_comments_key()] = value


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    process: Process,
    is_editable: bool,
    force_update: bool,
):

    session_state_manager.add_persistent_keys(get_text_input_process_name_key())
    if not is_editable or force_update:
        set_text_input_process_name(process.name)

    process.name = streamlit.text_input(
        "Process Name",
        key=get_text_input_process_name_key(),
        width=750,
        disabled=not is_editable,
    )

    session_state_manager.add_persistent_keys(get_text_area_process_comments_key())
    if not is_editable or force_update:
        set_text_area_process_comments(process.comments)

    process.comments = streamlit.text_area(
        "Comments",
        key=get_text_area_process_comments_key(),
        height=500,
        width=750,
        disabled=not is_editable,
    )
