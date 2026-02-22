import streamlit
from utils import SessionStateManager

import webapp.state.workcell_process_metadata_tab_state as state
from orm.workcell_process.models import Process


#
# TAB
#
def render(
    session_state_manager: SessionStateManager,
    process: Process,
    is_editable: bool,
    force_update: bool,
):

    session_state_manager.add_persistent_keys(state.TextInputProcessName.key())
    if not is_editable or force_update:
        state.TextInputProcessName.set(process.name)

    process.name = streamlit.text_input(
        "Process Name",
        key=state.TextInputProcessName.key(),
        width=750,
        disabled=not is_editable,
    )

    session_state_manager.add_persistent_keys(state.TextAreaProcessComments.key())
    if not is_editable or force_update:
        state.TextAreaProcessComments.set(process.comments)

    process.comments = streamlit.text_area(
        "Comments",
        key=state.TextAreaProcessComments.key(),
        height=500,
        width=750,
        disabled=not is_editable,
    )
