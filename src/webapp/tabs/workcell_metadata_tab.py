import streamlit
from utils import SessionStateManager

from orm.workcell.models import Workcell

_TAB_PREFIX = "workcell_metadata_tab"


#
# WORKCELL_METADATA_TAB_IS_EDITABLE
#
def get_workcell_metadata_tab_is_editable_key() -> str:
    return f"{_TAB_PREFIX}_is_editable"


def set_workcell_metadata_tab_is_editable(value: bool):
    streamlit.session_state[f"{_TAB_PREFIX}_is_editable"] = value


def get_workcell_metadata_tab_is_editable() -> bool:
    return streamlit.session_state.get(f"{_TAB_PREFIX}_is_editable", False)


#
# BUTTON CALLBACKS
#
def callback_button_workcell_metadata_tab_enable_edits():
    set_workcell_metadata_tab_is_editable(True)


def callback_button_workcell_metadata_tab_discard_edits():
    set_workcell_metadata_tab_is_editable(False)


def callback_button_workcell_metadata_tab_save_edits(workcell: Workcell):
    workcell.name = get_workcell_name_field()
    workcell.comments = get_workcell_comments_field()
    workcell.save()

    from pages.workcells import set_workcell_selectbox

    set_workcell_selectbox(workcell)

    set_workcell_metadata_tab_is_editable(False)


#
# WORKCELL NAME
#
def get_workcell_name_field_key() -> str:
    return f"text_input_{_TAB_PREFIX}_workcell_name"


def get_workcell_name_field() -> str:
    return streamlit.session_state[get_workcell_name_field_key()]


def set_workcell_name_field(value: str):
    streamlit.session_state[get_workcell_name_field_key()] = value


#
# WORKCELL COMMENTS
#
def get_workcell_comments_field_key() -> str:
    return f"text_area_{_TAB_PREFIX}_workcell_comments"


def get_workcell_comments_field() -> str:
    return streamlit.session_state[get_workcell_comments_field_key()]


def set_workcell_comments_field(value: str):
    streamlit.session_state[get_workcell_comments_field_key()] = value


#
# TAB
#
def render_workcell_metadata_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(get_workcell_metadata_tab_is_editable_key())

    with streamlit.container(horizontal=True):
        if not get_workcell_metadata_tab_is_editable():
            streamlit.button(
                "Enable Edits",
                key=f"button_{_TAB_PREFIX}_enable_edits",
                on_click=callback_button_workcell_metadata_tab_enable_edits,
                width=120,
            )

        else:
            streamlit.button(
                "Discard Edits",
                key=f"button_{_TAB_PREFIX}_discard_edits",
                on_click=callback_button_workcell_metadata_tab_discard_edits,
                width=120,
            )
            streamlit.button(
                "Save Edits",
                key=f"button_{_TAB_PREFIX}_save_edits",
                on_click=callback_button_workcell_metadata_tab_save_edits,
                args=(workcell,),
                width=120,
            )

    session_state_manager.add_persistent_keys(get_workcell_name_field_key())
    if not get_workcell_metadata_tab_is_editable():
        set_workcell_name_field(workcell.name)

    streamlit.text_input(
        "Workcell Name",
        value=workcell.name,
        key=get_workcell_name_field_key(),
        width=750,
        disabled=not get_workcell_metadata_tab_is_editable(),
    )

    session_state_manager.add_persistent_keys(get_workcell_comments_field_key())
    if not get_workcell_metadata_tab_is_editable():
        set_workcell_comments_field(workcell.comments)

    streamlit.text_area(
        "Comments",
        value=workcell.comments,
        key=get_workcell_comments_field_key(),
        height=500,
        width=750,
        disabled=not get_workcell_metadata_tab_is_editable(),
    )
