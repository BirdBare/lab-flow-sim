import streamlit
from utils import SessionStateManager

import webapp.state.workcell_process_metadata_tab_state as state
from orm.workcell_process.models import Process


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    process: Process,
    is_editable: bool,
    force_update: bool,
):

    session_state_manager.add_persistent_keys(state.get_text_input_process_name_key())
    if not is_editable or force_update:
        state.set_text_input_process_name(process.name)

    process.name = streamlit.text_input(
        "Process Name",
        key=state.get_text_input_process_name_key(),
        width=750,
        disabled=not is_editable,
    )

    session_state_manager.add_persistent_keys(state.get_text_area_process_comments_key())
    if not is_editable or force_update:
        state.set_text_area_process_comments(process.comments)

    process.comments = streamlit.text_area(
        "Comments",
        key=state.get_text_area_process_comments_key(),
        height=500,
        width=750,
        disabled=not is_editable,
    )
