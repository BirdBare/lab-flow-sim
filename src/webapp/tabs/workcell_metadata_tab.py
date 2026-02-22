import streamlit
from utils import SessionStateManager

import webapp.state.workcell_metadata_tab_state as state
from orm.workcell.models import Workcell


#
# BUTTON CALLBACKS
#
def callback_button_enable_edits():
    state.IsEditable.set(True)


def callback_button_discard_edits():
    state.IsEditable.set(False)


def callback_button_save_edits(workcell: Workcell):
    workcell.save()

    # This is a really crappy circular import bug I have to work around... #TODO
    streamlit.session_state["selectbox_workcell"] = workcell

    state.IsEditable.set(False)


#
# TAB
#
def render(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):

    session_state_manager.add_persistent_keys(state.IsEditable.key())

    with streamlit.container(horizontal=True):
        if not state.IsEditable.get():
            streamlit.button(
                "Enable Edits",
                key=f"{state.KEY_PREFIX}_button_enable_edits",
                on_click=callback_button_enable_edits,
                width=120,
            )

        else:
            streamlit.button(
                "Discard Edits",
                key=f"{state.KEY_PREFIX}_button_discard_edits",
                on_click=callback_button_discard_edits,
                width=120,
            )
            streamlit.button(
                "Save Edits",
                key=f"{state.KEY_PREFIX}_button_save_edits",
                on_click=callback_button_save_edits,
                args=(workcell,),
                width=120,
            )

    session_state_manager.add_persistent_keys(state.TextInputWorkcellName.key())
    if not state.IsEditable.get():
        state.TextInputWorkcellName.set(workcell.name)

    workcell.name = streamlit.text_input(
        "Workcell Name",
        key=state.TextInputWorkcellName.key(),
        width=750,
        disabled=not state.IsEditable.get(),
    )

    session_state_manager.add_persistent_keys(state.TextAreaWorkcellComments.key())
    if not state.IsEditable.get():
        state.TextAreaWorkcellComments.set(workcell.comments)

    workcell.comments = streamlit.text_area(
        "Comments",
        key=state.TextAreaWorkcellComments.key(),
        height=500,
        width=750,
        disabled=not state.IsEditable.get(),
    )
