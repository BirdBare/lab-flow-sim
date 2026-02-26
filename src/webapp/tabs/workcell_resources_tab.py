import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager

from orm.workcell.models import Resource, Workcell
from webapp.state import workcell_resource_tab_state as state


@streamlit.dialog("Resource Editor", dismissible=False)
def edit_resource(resource: Resource):
    with streamlit.container(gap=None):
        resource.name = streamlit.text_input("Device Name", value=resource.name, key=f"labware_{resource.id}_name")

        streamlit.divider()

    with streamlit.container(horizontal=True):
        if streamlit.button("Cancel"):
            state.DialogIsShown.set(False)
            streamlit.rerun()

        if not resource._state.adding:
            if streamlit.button("Delete"):
                resource.delete()
                state.DialogIsShown.set(False)
                streamlit.rerun()

        if streamlit.button("Save"):
            resource.save()
            state.DialogIsShown.set(False)
            streamlit.rerun()


#
# TAB
#
def render(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(state.DialogIsShown.key())

    with streamlit.container(gap=None, horizontal_alignment="center"):
        if streamlit.button("New Resource"):
            state.DialogIsShown.set(True)
            edit_resource(Resource(name="New Resource", workcell=workcell))

    resources = list(Resource.objects.filter(workcell=workcell).order_by(Lower("name")).all())
    resource_chunks = [resources[i : i + 3] for i in range(0, len(resources), 3)]

    with streamlit.container(horizontal_alignment="center"):
        for resource_chunk in resource_chunks:
            columns = streamlit.columns(3, width=1000)
            for column_index, resource in enumerate(resource_chunk):
                with columns[column_index], streamlit.container(border=True):
                    with streamlit.container(gap=None, horizontal_alignment="center"):
                        streamlit.space()

                        if streamlit.button(resource.name, type="tertiary", key=f"labware_{resource.id}_edit"):
                            state.DialogIsShown.set(True)
                            edit_resource(resource)

                        streamlit.divider()

                    streamlit.space()
