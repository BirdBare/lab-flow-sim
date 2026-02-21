import streamlit
from streamlit_flow import StreamlitFlowEdge, StreamlitFlowNode, StreamlitFlowState

from orm.device.models import Device
from orm.flow_diagram.models import AssignedDeviceNode
from orm.workcell.models import AssignedDevice, DeviceConnection, Workcell

_KEY_PREFIX = "workcell_diagram"


#
# WORKCELL_IS_EDITABLE
#
def get_is_editable_key() -> str:
    return f"{_KEY_PREFIX}_is_editable"


def set_is_editable(value: bool):
    streamlit.session_state[get_is_editable_key()] = value


def get_is_editable() -> bool:
    return streamlit.session_state.get(get_is_editable_key(), False)


#
# WORKCELL_STREAMLIT_FLOW_SELECTED_ID
#
def get_streamlit_flow_selected_id_key() -> str:
    return f"{_KEY_PREFIX}_streamlit_flow_selected_id"


def set_streamlit_flow_selected_id(value: None | str):
    streamlit.session_state[get_streamlit_flow_selected_id_key()] = value


def get_streamlit_flow_selected_id() -> None | str:
    return streamlit.session_state.get(get_streamlit_flow_selected_id_key(), None)


#
# WORKCELL_STREAMLIT_FLOW_NODE_KEY
#
def get_flow_node_dict_key() -> str:
    return f"{_KEY_PREFIX}_streamlit_flow_node_dict"


def get_flow_node_dict() -> dict[str, StreamlitFlowNode]:
    if get_flow_node_dict_key() not in streamlit.session_state:
        streamlit.session_state[get_flow_node_dict_key()] = {}

    return streamlit.session_state[get_flow_node_dict_key()]


#
# WORKCELL_STREAMLIT_ASSIGNED_DEVICE_KEY
#
def get_assigned_device_dict_key() -> str:
    return f"{_KEY_PREFIX}_assigned_device_dict"


def get_assigned_device_dict() -> dict[str, AssignedDevice]:
    if get_assigned_device_dict_key() not in streamlit.session_state:
        streamlit.session_state[get_assigned_device_dict_key()] = {}

    return streamlit.session_state[get_assigned_device_dict_key()]


#
# WORKCELL_STREAMLIT_FLOW_STATE
#
def get_streamlit_flow_state_key() -> str:
    return f"{_KEY_PREFIX}_streamlit_flow_state"


def set_streamlit_flow_state(workcell_streamlit_flow_state: StreamlitFlowState):
    streamlit.session_state[get_streamlit_flow_state_key()] = workcell_streamlit_flow_state


def get_streamlit_flow_state() -> StreamlitFlowState:
    if get_streamlit_flow_state_key() not in streamlit.session_state:
        set_streamlit_flow_state(StreamlitFlowState([], []))

    return streamlit.session_state[get_streamlit_flow_state_key()]


def reset_streamlit_flow_state(workcell: Workcell):
    set_streamlit_flow_selected_id(None)

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

        get_assigned_device_dict()[node.id] = assigned_device
        get_flow_node_dict()[node.id] = node

        nodes.append(node)

    for device_connection in DeviceConnection.objects.filter(assigned_devices__in=assigned_devices).distinct().all():
        connected_devices = list(device_connection.assigned_devices.all())

        device_1 = connected_devices[0]
        db_node_1 = AssignedDeviceNode.objects.filter(assigned_device=device_1).get().node

        device_2 = connected_devices[1]
        db_node_2 = AssignedDeviceNode.objects.filter(assigned_device=device_2).get().node

        edge = StreamlitFlowEdge(f"{db_node_1.id}-{db_node_2.id}", str(db_node_1.id), str(db_node_2.id))

        edges.append(edge)

    get_streamlit_flow_state().nodes = nodes
    get_streamlit_flow_state().edges = edges


#
# SELECT BOX NODE ASSIGNED DEVICE
#
def get_selectbox_device_key() -> str:
    return "selectbox_device"


def get_selectbox_device() -> Device:
    return streamlit.session_state[get_selectbox_device_key()]
