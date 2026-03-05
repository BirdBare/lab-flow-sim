import typing
import uuid

import streamlit
import streamlit_flow
from utils import SessionStateManager

import webapp.state.workcell_layout_tab_state as state
from orm.device.models import Device
from orm.flow_diagram.models import AssignedDeviceNode
from orm.workcell.models import AssignedDevice, DeviceConnection, Workcell


def build_streamlit_flow_state(workcell: Workcell):
    state.StreamlitFlowSelectedID.set(None)

    handle_by_db_id: dict[uuid.UUID, streamlit_flow.Handle] = {}
    node_by_db_id: dict[uuid.UUID, streamlit_flow.BaseNode] = {}
    edge_by_db_id: dict[uuid.UUID, streamlit_flow.Edge] = {}

    assigned_devices = list(
        AssignedDevice.objects.filter(
            workcell=workcell,
        ).all(),
    )

    # build handles and nodes
    for assigned_device in assigned_devices:
        assigned_device_node = AssignedDeviceNode.objects.filter(assigned_device=assigned_device).get()
        db_node = assigned_device_node.node

        node_handles: list[streamlit_flow.Handle] = []

        # handles for node
        for db_handle in db_node.handles.all():
            if db_handle.id in handle_by_db_id:
                handle = handle_by_db_id[db_handle.id]

            else:
                handle = handle_by_db_id[db_handle.id] = streamlit_flow.Handle(
                    typing.cast("typing.Literal['top', 'bottom', 'left', 'right']", db_handle.position),
                    is_source=db_handle.is_source,
                    is_target=db_handle.is_target,
                )

            node_handles.append(handle)

        # node
        node = streamlit_flow.MarkdownNode(db_node.x_pos, db_node.y_pos, "", handles=node_handles)

        state.AssignedDeviceByNodeID.get()[node.id] = assigned_device
        node_by_db_id[db_node.id] = node

    for device_connection in []:
        device_1 = device_connection.device_1
        db_node_1 = AssignedDeviceNode.objects.filter(assigned_device=device_1).get().node

        device_2 = device_connection.device_2
        db_node_2 = AssignedDeviceNode.objects.filter(assigned_device=device_2).get().node

        edge = streamlit_flow.Edge(f"{db_node_1.id}-{db_node_2.id}", str(db_node_1.id), str(db_node_2.id))

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

    state.AssignedDeviceByNodeID.get()[new_node.id] = new_assigned_device
    state.StreamlitFlowState.get().nodes.append(new_node)

    state.StreamlitFlowSelectedID.set(new_node.id)


def callback_selectbox_set_assigned_device_device(assigned_device: AssignedDevice):
    device = state.SelectboxAssignedDeviceDevice.get()
    if device is None:
        return

    assigned_device.device = device


def callback_number_input_set_device_connection_distance(device_connection: DeviceConnection):
    device_connection.distance = state.NumberInputDeviceConnectionDistance.get()


def callback_button_deselect():
    state.StreamlitFlowSelectedID.set(None)


def callback_button_delete_node():
    state.StreamlitFlowState.get().nodes = [
        node for node in state.StreamlitFlowState.get().nodes if node.id != state.StreamlitFlowSelectedID.get()
    ]
    state.StreamlitFlowSelectedID.set(None)


def callback_button_delete_edge():
    state.StreamlitFlowState.get().edges = [
        edge for edge in state.StreamlitFlowState.get().edges if edge.id != state.StreamlitFlowSelectedID.get()
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
        state.ForceUpdate.key(),
        state.StreamlitFlowState.key(),
        state.StreamlitFlowSelectedID.key(),
        state.AssignedDeviceByNodeID.key(),
        state.DeviceConnectionByEdgeID.key(),
        state.SelectboxAssignedDeviceDevice.key(),
        state.NumberInputDeviceConnectionDistance.key(),
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
            node.data = {"content": state.AssignedDeviceByNodeID.get()[node.id].device.name}
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

    for edge in state.StreamlitFlowState.get().edges:
        device_connection = state.DeviceConnectionByEdgeID.get()[edge.id]

        edge.label = f"Distance: {device_connection.distance}"
        edge.label_show_bg = True
        edge.label_style = {"color": "black"}

        if edge.id == state.StreamlitFlowSelectedID.get():
            edge.style = {"stroke": "red"}
        else:
            edge.style = {"stroke": "white"}

    # Create the canvas
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

    # Capture new edges
    for edge in state.StreamlitFlowState.get().edges:
        if edge.id not in state.DeviceConnectionByEdgeID.get():
            source_assigned_device = state.AssignedDeviceByNodeID.get()[edge.source]
            target_assigned_device = state.AssignedDeviceByNodeID.get()[edge.target]

            new_device_connection = DeviceConnection(
                device_1=source_assigned_device,
                device_2=target_assigned_device,
                distance=0,
            )

            state.DeviceConnectionByEdgeID.get()[edge.id] = new_device_connection

            state.StreamlitFlowState.get().selected_id = edge.id

    if state.IsEditable.get():
        if state.StreamlitFlowState.get().selected_id is not None:
            state.StreamlitFlowSelectedID.set(state.StreamlitFlowState.get().selected_id)
            state.StreamlitFlowState.get().selected_id = None  # type:ignore

            state.ForceUpdate.set(True)

            streamlit.rerun()

    if state.IsEditable.get():
        with streamlit.sidebar:
            selected_id = state.StreamlitFlowSelectedID.get()
            if selected_id is None:
                streamlit.title("Canvas Configuration")

                streamlit.button("Add Device", width=100, on_click=callback_button_add_device, args=(workcell,))

            elif selected_id in state.AssignedDeviceByNodeID.get():
                assigned_device = state.AssignedDeviceByNodeID.get()[selected_id]

                streamlit.title("Node Configuration")

                devices = list(Device.objects.all())

                try:
                    device = assigned_device.device
                    device_index = devices.index(device)
                except AssignedDevice.device.RelatedObjectDoesNotExist:
                    device = None
                    device_index = None

                if state.ForceUpdate.get():
                    state.SelectboxAssignedDeviceDevice.set(device)

                streamlit.selectbox(
                    "Device",
                    devices,
                    index=device_index,
                    format_func=lambda device: device.name,
                    on_change=callback_selectbox_set_assigned_device_device,
                    key=state.SelectboxAssignedDeviceDevice.key(),
                    args=(assigned_device,),
                )

                with streamlit.container(horizontal=True, horizontal_alignment="center"):
                    streamlit.button("Deselect", width=100, on_click=callback_button_deselect)
                    streamlit.button("Delete", width=100, on_click=callback_button_delete_node)

            elif selected_id in state.DeviceConnectionByEdgeID.get():
                device_connection = state.DeviceConnectionByEdgeID.get()[selected_id]

                streamlit.title("Edge Configuration")

                if state.ForceUpdate.get():
                    state.NumberInputDeviceConnectionDistance.set(device_connection.distance)

                streamlit.number_input(
                    "Distance",
                    min_value=0,
                    step=1,
                    on_change=callback_number_input_set_device_connection_distance,
                    args=(device_connection,),
                    key=state.NumberInputDeviceConnectionDistance.key(),
                )

                with streamlit.container(horizontal=True, horizontal_alignment="center"):
                    streamlit.button("Deselect", width=100, on_click=callback_button_deselect)
                    streamlit.button("Delete", width=100, on_click=callback_button_delete_edge)

    state.ForceUpdate.set(False)
