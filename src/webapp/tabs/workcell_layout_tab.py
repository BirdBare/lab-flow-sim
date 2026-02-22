import uuid

import streamlit
from streamlit_flow import StreamlitFlowEdge, StreamlitFlowNode, streamlit_flow
from utils import SessionStateManager

import webapp.state.workcell_layout_tab_state as state
from orm.device.models import Device
from orm.flow_diagram.models import AssignedDeviceNode
from orm.workcell.models import AssignedDevice, DeviceConnection, Workcell
from webapp.state import workcell_labware_tab_state


def build_streamlit_flow_state(workcell: Workcell):
    state.StreamlitFlowSelectedID.set(None)

    nodes: list[StreamlitFlowNode] = []
    edges: list[StreamlitFlowEdge] = []

    assigned_devices = AssignedDevice.objects.filter(
        workcell=workcell,
    ).all()

    for assigned_device in assigned_devices:
        db_node = AssignedDeviceNode.objects.filter(assigned_device=assigned_device).get().node

        node = StreamlitFlowNode(
            str(db_node.id),
            (db_node.x_pos, db_node.y_pos),
            {"content": ""},
        )

        state.AssignedDeviceDict.get()[node.id] = assigned_device
        state.StreamlitFlowNodeDict.get()[node.id] = node

        nodes.append(node)

    for device_connection in DeviceConnection.objects.filter(assigned_devices__in=assigned_devices).distinct().all():
        connected_devices = list(device_connection.assigned_devices.all())

        device_1 = connected_devices[0]
        db_node_1 = AssignedDeviceNode.objects.filter(assigned_device=device_1).get().node

        device_2 = connected_devices[1]
        db_node_2 = AssignedDeviceNode.objects.filter(assigned_device=device_2).get().node

        edge = StreamlitFlowEdge(f"{db_node_1.id}-{db_node_2.id}", str(db_node_1.id), str(db_node_2.id))

        edges.append(edge)

    state.StreamlitFlowState.get().nodes = nodes
    state.StreamlitFlowState.get().edges = edges


#
# BUTTON CALLBACKS
#
def callback_button_enable_edits():
    state.IsEditable.set(True)


def callback_button_discard_edits(workcell: Workcell):
    state.IsEditable.set(False)


def callback_button_save_edits(workcell: Workcell):
    state.IsEditable.set(False)


def callback_button_add_device(workcell: Workcell):
    new_assigned_device = AssignedDevice(workcell=workcell, device=None)

    new_node = StreamlitFlowNode(
        str(uuid.uuid4()),
        (0, 0),
        {"content": "New"},
    )

    state.AssignedDeviceDict.get()[new_node.id] = new_assigned_device
    state.StreamlitFlowState.get().nodes.append(new_node)

    state.StreamlitFlowSelectedID.set(new_node.id)


def callback_button_set_assigned_device_device(assigned_device: AssignedDevice):
    device = state.SelectboxDevice.get()
    if device is None:
        return

    assigned_device.device = device


def callback_button_deselect():
    state.StreamlitFlowSelectedID.set(None)


def callback_button_delete():
    state.StreamlitFlowState.get().nodes = [
        node for node in state.StreamlitFlowState.get().nodes if node.id != state.StreamlitFlowSelectedID.get()
    ]
    state.StreamlitFlowSelectedID.set(None)


#
# TAB
#
def render(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(
        state.IsEditable.key(),
        state.StreamlitFlowState.key(),
        state.StreamlitFlowSelectedID.key(),
        state.AssignedDeviceDict.key(),
        state.StreamlitFlowNodeDict.key(),
        state.SelectboxDevice.key(),
    )

    if not state.IsEditable.get():
        build_streamlit_flow_state(workcell)

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
                args=(workcell,),
                width=120,
            )
            streamlit.button(
                "Save Edits",
                key=f"{state.KEY_PREFIX}_button_save_edits",
                on_click=callback_button_save_edits,
                args=(workcell,),
                width=120,
            )

    for node in state.StreamlitFlowState.get().nodes:
        node.draggable = state.IsEditable.get()

        try:
            node.data = {"content": state.AssignedDeviceDict.get()[node.id].device.name}
        except AssignedDevice.device.RelatedObjectDoesNotExist:
            node.data = {"content": "Configure in sidebar"}

        if node.id == state.StreamlitFlowSelectedID.get():
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
    if not workcell_labware_tab_state.DialogIsShown.get():
        state.StreamlitFlowState.set(
            streamlit_flow(
                "workcell_device_diagram",
                state.StreamlitFlowState.get(),
                allow_new_edges=state.IsEditable.get(),
                get_node_on_click=state.IsEditable.get(),
                get_edge_on_click=state.IsEditable.get(),
                enable_pane_menu=state.IsEditable.get(),
                hide_watermark=True,
            ),
        )

    if state.IsEditable.get():
        if state.StreamlitFlowState.get().selected_id is not None:
            state.StreamlitFlowSelectedID.set(state.StreamlitFlowState.get().selected_id)
            state.StreamlitFlowState.get().selected_id = None  # type:ignore
            streamlit.rerun()

        with streamlit.sidebar:
            selected_id = state.StreamlitFlowSelectedID.get()
            if selected_id is None:
                streamlit.title("Canvas Configuration")

                streamlit.button("Add Device", width=100, on_click=callback_button_add_device, args=(workcell,))

            else:
                if selected_id in state.AssignedDeviceDict.get():
                    assigned_device = state.AssignedDeviceDict.get()[selected_id]

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
                        key=state.SelectboxDevice.key(),
                        args=(assigned_device,),
                    )

                with streamlit.container(horizontal=True, horizontal_alignment="center"):
                    streamlit.button("Deselect", width=100, on_click=callback_button_deselect)
                    streamlit.button("Delete", width=100, on_click=callback_button_delete)
