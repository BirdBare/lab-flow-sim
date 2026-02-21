import streamlit

from orm.workcell_process.models import Process

_KEY_PREFIX = "workcell_processes"


#
# IS_EDITABLE
#
def get_is_editable_key() -> str:
    return f"{_KEY_PREFIX}_is_editable"


def set_is_editable(value: bool):
    streamlit.session_state[get_is_editable_key()] = value


def get_is_editable() -> bool:
    return streamlit.session_state.get(get_is_editable_key(), False)


#
# FORCE UPDATE
#
def get_force_update_key() -> str:
    return f"{_KEY_PREFIX}_force_update"


def get_force_update() -> bool:
    return streamlit.session_state.get(get_force_update_key(), False)


def set_force_update(value: bool):
    streamlit.session_state[get_force_update_key()] = value


#
# Processes
#
def get_processes_key() -> str:
    return f"{_KEY_PREFIX}_processes"


def get_processes() -> list[Process]:
    if get_processes_key() not in streamlit.session_state:
        reset_processes()

    return streamlit.session_state[get_processes_key()]


def reset_processes():
    streamlit.session_state[get_processes_key()] = []


#
# SELECTBOX_PROCESS
#
def get_selectbox_process_key() -> str:
    return f"{_KEY_PREFIX}_selectbox_process"


def set_selectbox_process(value: Process):
    streamlit.session_state[get_selectbox_process_key()] = value


def get_selectbox_process() -> Process:
    return streamlit.session_state.get(get_selectbox_process_key(), False)
