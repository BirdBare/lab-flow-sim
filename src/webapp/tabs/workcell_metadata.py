import streamlit
from utils import SessionStateManager

from orm.workcell.models import Workcell

_TAB_PREFIX = "workcell_metadata"


#
# WORKCELL_METADATA_TAB_IS_EDITABLE
#
def get_is_editable_key() -> str:
    return f"{_TAB_PREFIX}_is_editable"


def set_is_editable(value: bool):
    streamlit.session_state[get_is_editable_key()] = value


def get_is_editable() -> bool:
    return streamlit.session_state.get(get_is_editable_key(), False)


#
# BUTTON CALLBACKS
#
def callback_button_enable_edits():
    set_is_editable(True)


def callback_button_discard_edits():
    set_is_editable(False)


def callback_button_save_edits():
    from pages.workcells import get_selectbox_workcell, set_selectbox_workcell

    workcell = get_selectbox_workcell()
    workcell.name = get_text_input_workcell_name()
    workcell.comments = get_text_area_workcell_comments()
    workcell.save()

    set_selectbox_workcell(workcell)

    set_is_editable(False)


#
# WORKCELL NAME
#
def get_text_input_workcell_name_key() -> str:
    return f"{_TAB_PREFIX}_text_input_workcell_name"


def get_text_input_workcell_name() -> str:
    return streamlit.session_state[get_text_input_workcell_name_key()]


def set_text_input_workcell_name(value: str):
    streamlit.session_state[get_text_input_workcell_name_key()] = value


#
# WORKCELL COMMENTS
#
def get_text_area_workcell_comments_key() -> str:
    return f"{_TAB_PREFIX}_text_area_workcell_comments"


def get_text_area_workcell_comments() -> str:
    return streamlit.session_state[get_text_area_workcell_comments_key()]


def set_text_area_workcell_comments(value: str):
    streamlit.session_state[get_text_area_workcell_comments_key()] = value


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(get_is_editable_key())

    with streamlit.container(horizontal=True):
        if not get_is_editable():
            streamlit.button(
                "Enable Edits",
                key=f"button_{_TAB_PREFIX}_enable_edits",
                on_click=callback_button_enable_edits,
                width=120,
            )

        else:
            streamlit.button(
                "Discard Edits",
                key=f"button_{_TAB_PREFIX}_discard_edits",
                on_click=callback_button_discard_edits,
                width=120,
            )
            streamlit.button(
                "Save Edits",
                key=f"button_{_TAB_PREFIX}_save_edits",
                on_click=callback_button_save_edits,
                width=120,
            )

    session_state_manager.add_persistent_keys(get_text_input_workcell_name_key())
    if not get_is_editable():
        set_text_input_workcell_name(workcell.name)

    streamlit.text_input(
        "Workcell Name",
        value=workcell.name,
        key=get_text_input_workcell_name_key(),
        width=750,
        disabled=not get_is_editable(),
    )

    session_state_manager.add_persistent_keys(get_text_area_workcell_comments_key())
    if not get_is_editable():
        set_text_area_workcell_comments(workcell.comments)

    streamlit.text_area(
        "Comments",
        value=workcell.comments,
        key=get_text_area_workcell_comments_key(),
        height=500,
        width=750,
        disabled=not get_is_editable(),
    )
