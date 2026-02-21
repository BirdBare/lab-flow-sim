import uuid

import streamlit
from streamlit_flow import StreamlitFlowNode, streamlit_flow
from utils import SessionStateManager

import webapp.state.workcell_layout_tab_state as state
from orm.device.models import Device
from orm.workcell.models import AssignedDevice, Workcell
from webapp.state import workcell_labware_tab_state


#
# BUTTON CALLBACKS
#
def callback_button_enable_edits():
    state.set_is_editable(True)


def callback_button_discard_edits(workcell: Workcell):
    state.set_is_editable(False)


def callback_button_save_edits(workcell: Workcell):
    state.set_is_editable(False)


def callback_button_add_device(workcell: Workcell):
    new_assigned_device = AssignedDevice(workcell=workcell, device=None)

    new_node = StreamlitFlowNode(
        str(uuid.uuid4()),
        (0, 0),
        {"content": "New"},
    )

    state.get_assigned_device_dict()[new_node.id] = new_assigned_device
    state.get_streamlit_flow_state().nodes.append(new_node)

    state.set_streamlit_flow_selected_id(new_node.id)


def callback_button_set_assigned_device_device(assigned_device: AssignedDevice):
    assigned_device.device = state.get_selectbox_device()


def callback_button_deselect():
    state.set_streamlit_flow_selected_id(None)


def callback_button_delete():
    state.get_streamlit_flow_state().nodes = [
        node for node in state.get_streamlit_flow_state().nodes if node.id != state.get_streamlit_flow_selected_id()
    ]
    state.set_streamlit_flow_selected_id(None)


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    if not state.get_is_editable():
        state.reset_streamlit_flow_state(workcell)

    session_state_manager.add_persistent_keys(
        state.get_is_editable_key(),
        state.get_streamlit_flow_state_key(),
        state.get_streamlit_flow_selected_id_key(),
        state.get_assigned_device_dict_key(),
        state.get_flow_node_dict_key(),
        state.get_selectbox_device_key(),
    )

    with streamlit.container(horizontal=True):
        if not state.get_is_editable():
            streamlit.button(
                "Enable Edits",
                key=f"button_{state._KEY_PREFIX}_enable_edits",
                on_click=callback_button_enable_edits,
                width=120,
            )

        else:
            streamlit.button(
                "Discard Edits",
                key=f"button_{state._KEY_PREFIX}_discard_edits",
                on_click=callback_button_discard_edits,
                args=(workcell,),
                width=120,
            )
            streamlit.button(
                "Save Edits",
                key=f"button_{state._KEY_PREFIX}_save_edits",
                on_click=callback_button_save_edits,
                args=(workcell,),
                width=120,
            )

    for node in state.get_streamlit_flow_state().nodes:
        node.draggable = state.get_is_editable()

        try:
            node.data = {"content": state.get_assigned_device_dict()[node.id].device.name}
        except AssignedDevice.device.RelatedObjectDoesNotExist:
            node.data = {"content": "Configure in sidebar"}

        if node.id == state.get_streamlit_flow_selected_id():
            node.style = {
                "width": "auto",
                "height": "auto",
                "borderStyle": "solid",
                "borderWidth": "Thick",
                "borderColor": "red",
            }
        else:
            node.style = {
                "width": "auto",
                "height": "auto",
            }

    # Create the canvas
    if not workcell_labware_tab_state.get_dialog_is_shown():
        state.set_streamlit_flow_state(
            streamlit_flow(
                "workcell_device_diagram",
                state.get_streamlit_flow_state(),
                allow_new_edges=state.get_is_editable(),
                get_node_on_click=state.get_is_editable(),
                get_edge_on_click=state.get_is_editable(),
                enable_pane_menu=state.get_is_editable(),
                hide_watermark=True,
            ),
        )

    if state.get_is_editable():
        if state.get_streamlit_flow_state().selected_id is not None:
            state.set_streamlit_flow_selected_id(state.get_streamlit_flow_state().selected_id)
            state.get_streamlit_flow_state().selected_id = None  # type:ignore
            streamlit.rerun()

        with streamlit.sidebar:
            selected_id = state.get_streamlit_flow_selected_id()
            if selected_id is None:
                streamlit.title("Canvas Configuration")

                streamlit.button("Add Device", width=100, on_click=callback_button_add_device, args=(workcell,))

            else:
                if selected_id in state.get_assigned_device_dict():
                    assigned_device = state.get_assigned_device_dict()[selected_id]

                    streamlit.title("Node Configuration")

                    devices = list(Device.objects.all())

                    try:
                        device_index = devices.index(assigned_device.device)
                    except AssignedDevice.device.RelatedObjectDoesNotExist:
                        device_index = None

                    streamlit.selectbox(
                        "Device",
                        devices,
                        index=device_index,
                        format_func=lambda device: device.name,
                        on_change=callback_button_set_assigned_device_device,
                        key="selectbox_device",
                        args=(assigned_device,),
                    )

                with streamlit.container(horizontal=True, horizontal_alignment="center"):
                    streamlit.button("Deselect", width=100, on_click=callback_button_deselect)
                    streamlit.button("Delete", width=100, on_click=callback_button_delete)
