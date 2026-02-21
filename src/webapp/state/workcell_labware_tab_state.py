import streamlit

_KEY_PREFIX = "workcell_labware"


def get_dialog_is_shown_key() -> str:
    return f"{_KEY_PREFIX}_dialog_is_show"


def get_dialog_is_shown() -> bool:
    return streamlit.session_state.get(get_dialog_is_shown_key(), False)


def set_dialog_is_shown(value: bool):
    streamlit.session_state[get_dialog_is_shown_key()] = value
