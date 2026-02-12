import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager

from orm.labware.models import Labware
from orm.workcell.models import Workcell

_KEY_PREFIX = "workcell_labware"


def get_dialog_is_shown_key() -> str:
    return f"{_KEY_PREFIX}_dialog_is_show"


def get_dialog_is_shown() -> bool:
    return streamlit.session_state.get(get_dialog_is_shown_key(), False)


def set_dialog_is_shown(value: bool):
    streamlit.session_state[get_dialog_is_shown_key()] = value


@streamlit.dialog("Labware Editor", dismissible=False)
def edit_labware(labware: Labware):
    with streamlit.container(gap=None):
        labware.name = streamlit.text_input("Device Name", value=labware.name, key=f"labware_{labware.id}_name")

        streamlit.divider()

    with streamlit.container(horizontal=True):
        if streamlit.button("Cancel"):
            set_dialog_is_shown(False)
            streamlit.rerun()

        if not labware._state.adding:
            if streamlit.button("Delete"):
                labware.delete()
                set_dialog_is_shown(False)
                streamlit.rerun()

        if streamlit.button("Save"):
            labware.save()
            set_dialog_is_shown(False)
            streamlit.rerun()


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(get_dialog_is_shown_key())

    with streamlit.container(gap=None, horizontal_alignment="center"):
        if streamlit.button("New Labware"):
            set_dialog_is_shown(True)
            edit_labware(Labware(name="New Labware", workcell=workcell))

    labwares = list(Labware.objects.filter(workcell=workcell).order_by(Lower("name")).all())
    labware_chunks = [labwares[i : i + 3] for i in range(0, len(labwares), 3)]

    with streamlit.container(horizontal_alignment="center"):
        for labware_chunk in labware_chunks:
            columns = streamlit.columns(3, width=1000)
            for column_index, labware in enumerate(labware_chunk):
                with columns[column_index], streamlit.container(border=True):
                    with streamlit.container(gap=None, horizontal_alignment="center"):
                        streamlit.space()

                        if streamlit.button(labware.name, type="tertiary", key=f"labware_{labware.id}_edit"):
                            set_dialog_is_shown(True)
                            edit_labware(labware)

                        streamlit.divider()

                    streamlit.space()
