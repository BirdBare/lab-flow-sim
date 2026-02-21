import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager

from orm.workcell.models import Labware, Workcell
from webapp.state import workcell_labware_tab_state as state


@streamlit.dialog("Labware Editor", dismissible=False)
def edit_labware(labware: Labware):
    with streamlit.container(gap=None):
        labware.name = streamlit.text_input("Device Name", value=labware.name, key=f"labware_{labware.id}_name")

        streamlit.divider()

    with streamlit.container(horizontal=True):
        if streamlit.button("Cancel"):
            state.set_dialog_is_shown(False)
            streamlit.rerun()

        if not labware._state.adding:
            if streamlit.button("Delete"):
                labware.delete()
                state.set_dialog_is_shown(False)
                streamlit.rerun()

        if streamlit.button("Save"):
            labware.save()
            state.set_dialog_is_shown(False)
            streamlit.rerun()


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(state.get_dialog_is_shown_key())

    with streamlit.container(gap=None, horizontal_alignment="center"):
        if streamlit.button("New Labware"):
            state.set_dialog_is_shown(True)
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
                            state.set_dialog_is_shown(True)
                            edit_labware(labware)

                        streamlit.divider()

                    streamlit.space()
