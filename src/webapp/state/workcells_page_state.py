import streamlit

from orm.workcell.models import Workcell


#
# WORKCELL SELECTBOX
#
def get_workcell_selectbox_key() -> str:
    return "selectbox_workcell"


def get_selectbox_workcell() -> Workcell:
    return streamlit.session_state[get_workcell_selectbox_key()]


def set_selectbox_workcell(workcell: Workcell):
    streamlit.session_state[get_workcell_selectbox_key()] = workcell
