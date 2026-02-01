import uuid

import streamlit
from streamlit_flow import StreamlitFlowEdge, StreamlitFlowNode, StreamlitFlowState, streamlit_flow
from utils import SessionStateManager

from orm.device.models import Device
from orm.flow_diagram.models import AssignedDeviceNode
from orm.workcell.models import AssignedDevice, DeviceConnection, Workcell


#
# WORKCELL_STREAMLIT_FLOW_SELECTED_ID
#
def set_workcell_streamlit_flow_selected_id(value: None | str):
    streamlit.session_state["workcell_streamlit_flow_selected_id"] = value


def get_workcell_streamlit_flow_selected_id() -> None | str:
    return streamlit.session_state.get("workcell_streamlit_flow_selected_id", None)


#
# WORKCELL_STREAMLIT_FLOW_NODE_KEY
#


def get_workcell_streamlit_flow_node_key() -> dict[str, StreamlitFlowNode]:
    if "workcell_streamlit_flow_node_key" not in streamlit.session_state:
        streamlit.session_state["workcell_streamlit_flow_node_key"] = {}

    return streamlit.session_state["workcell_streamlit_flow_node_key"]


#
# WORKCELL_STREAMLIT_ASSIGNED_DEVICE_KEY
#


def get_workcell_assigned_device_key() -> dict[str, AssignedDevice]:
    if "workcell_assigned_device_key" not in streamlit.session_state:
        streamlit.session_state["workcell_assigned_device_key"] = {}

    return streamlit.session_state["workcell_assigned_device_key"]


#
# WORKCELL_STREAMLIT_FLOW_STATE
#
def set_workcell_streamlit_flow_state(workcell_streamlit_flow_state: StreamlitFlowState):
    streamlit.session_state["workcell_streamlit_flow_state"] = workcell_streamlit_flow_state


def get_workcell_streamlit_flow_state() -> StreamlitFlowState:
    if "workcell_streamlit_flow_state" not in streamlit.session_state:
        set_workcell_streamlit_flow_state(StreamlitFlowState([], []))

    return streamlit.session_state["workcell_streamlit_flow_state"]


def reset_workcell_streamlit_flow_state(workcell: Workcell):
    set_workcell_streamlit_flow_selected_id(None)

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

        get_workcell_assigned_device_key()[node.id] = assigned_device
        get_workcell_streamlit_flow_node_key()[node.id] = node

        nodes.append(node)

    for device_connection in DeviceConnection.objects.filter(assigned_devices__in=assigned_devices).distinct().all():
        connected_devices = list(device_connection.assigned_devices.all())

        device_1 = connected_devices[0]
        db_node_1 = AssignedDeviceNode.objects.filter(assigned_device=device_1).get().node

        device_2 = connected_devices[1]
        db_node_2 = AssignedDeviceNode.objects.filter(assigned_device=device_2).get().node

        edge = StreamlitFlowEdge(f"{db_node_1.id}-{db_node_2.id}", str(db_node_1.id), str(db_node_2.id))

        edges.append(edge)

    get_workcell_streamlit_flow_state().nodes = nodes
    get_workcell_streamlit_flow_state().edges = edges


#
# TAB
#
def render_workcell_diagram_tab(
    session_state_manager: SessionStateManager,
    workcell_is_editable: bool,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(
        "workcell_streamlit_flow_state",
        "workcell_streamlit_flow_state_reset",
        "workcell_streamlit_flow_selected_id",
        "workcell_streamlit_flow_node_key",
        "workcell_assigned_device_key",
    )

    if streamlit.button("Add Device", width=100):
        new_assigned_device = AssignedDevice(workcell=workcell, device=None)

        new_node = StreamlitFlowNode(
            str(uuid.uuid4()),
            (0, 0),
            {"content": "New"},
        )

        get_workcell_assigned_device_key()[new_node.id] = new_assigned_device
        get_workcell_streamlit_flow_state().nodes.append(new_node)
        streamlit.rerun()

    for node in get_workcell_streamlit_flow_state().nodes:
        try:
            node.data = {"content": get_workcell_assigned_device_key()[node.id].device.name}
        except AssignedDevice.device.RelatedObjectDoesNotExist:
            node.data = {"content": "Configure in sidebar"}

        if node.id == get_workcell_streamlit_flow_selected_id():
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
    set_workcell_streamlit_flow_state(
        streamlit_flow(
            "workcell_device_diagram",
            get_workcell_streamlit_flow_state(),
            allow_new_edges=True,
            get_node_on_click=True,
            get_edge_on_click=True,
            enable_pane_menu=True,
        ),
    )

    if get_workcell_streamlit_flow_state().selected_id is not None:
        set_workcell_streamlit_flow_selected_id(get_workcell_streamlit_flow_state().selected_id)
        get_workcell_streamlit_flow_state().selected_id = None  # type:ignore
        streamlit.rerun()

    with streamlit.sidebar:
        selected_id = get_workcell_streamlit_flow_selected_id()
        if selected_id is not None:
            if selected_id in get_workcell_assigned_device_key():
                assigned_device = get_workcell_assigned_device_key()[selected_id]

                streamlit.title("Node Configuration")

                devices = list(Device.objects.all())

                try:
                    device_index = devices.index(assigned_device.device)
                except AssignedDevice.device.RelatedObjectDoesNotExist:
                    device_index = None

                def assign(ad):
                    ad.device = streamlit.session_state["selectbox_device"]

                streamlit.selectbox(
                    "Device",
                    devices,
                    index=device_index,
                    format_func=lambda device: device.name,
                    on_change=assign,
                    key="selectbox_device",
                    args=(assigned_device,),
                )

            def res():
                set_workcell_streamlit_flow_selected_id(None)

            def dele():
                clear_workcell_streamlit_flow_state()

            with streamlit.container(horizontal=True, horizontal_alignment="center"):
                streamlit.button("Deselect", width=100, on_click=res)
                streamlit.button("Delete", width=100, on_click=dele)

    streamlit.stop()
