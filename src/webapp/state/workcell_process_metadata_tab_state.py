import streamlit

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
