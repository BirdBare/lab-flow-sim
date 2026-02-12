import uuid

import streamlit
from streamlit_flow import StreamlitFlowEdge, StreamlitFlowNode, StreamlitFlowState, streamlit_flow
from utils import SessionStateManager

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


#
# BUTTON CALLBACKS
#
def callback_button_enable_edits():
    set_is_editable(True)


def callback_button_discard_edits():
    from pages.workcells import get_selectbox_workcell

    reset_streamlit_flow_state(get_selectbox_workcell())
    set_is_editable(False)


def callback_button_save_edits(workcell: Workcell):
    set_is_editable(False)


def callback_button_add_device(workcell: Workcell):
    new_assigned_device = AssignedDevice(workcell=workcell, device=None)

    new_node = StreamlitFlowNode(
        str(uuid.uuid4()),
        (0, 0),
        {"content": "New"},
    )

    get_assigned_device_dict()[new_node.id] = new_assigned_device
    get_streamlit_flow_state().nodes.append(new_node)

    set_streamlit_flow_selected_id(new_node.id)


def callback_button_set_assigned_device_device(assigned_device: AssignedDevice):
    assigned_device.device = get_selectbox_device()


def callback_button_deselect():
    set_streamlit_flow_selected_id(None)


def callback_button_delete():
    get_streamlit_flow_state().nodes = [
        node for node in get_streamlit_flow_state().nodes if node.id != get_streamlit_flow_selected_id()
    ]
    set_streamlit_flow_selected_id(None)


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    workcell: Workcell,
):
    session_state_manager.add_persistent_keys(
        get_is_editable_key(),
        get_streamlit_flow_state_key(),
        get_streamlit_flow_selected_id_key(),
        get_assigned_device_dict_key(),
        get_flow_node_dict_key(),
        get_selectbox_device_key(),
    )

    with streamlit.container(horizontal=True):
        if not get_is_editable():
            streamlit.button(
                "Enable Edits",
                key=f"button_{_KEY_PREFIX}_enable_edits",
                on_click=callback_button_enable_edits,
                width=120,
            )

        else:
            streamlit.button(
                "Discard Edits",
                key=f"button_{_KEY_PREFIX}_discard_edits",
                on_click=callback_button_discard_edits,
                width=120,
            )
            streamlit.button(
                "Save Edits",
                key=f"button_{_KEY_PREFIX}_save_edits",
                on_click=callback_button_save_edits,
                args=(workcell,),
                width=120,
            )

    for node in get_streamlit_flow_state().nodes:
        node.draggable = get_is_editable()

        try:
            node.data = {"content": get_assigned_device_dict()[node.id].device.name}
        except AssignedDevice.device.RelatedObjectDoesNotExist:
            node.data = {"content": "Configure in sidebar"}

        if node.id == get_streamlit_flow_selected_id():
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
    set_streamlit_flow_state(
        streamlit_flow(
            "workcell_device_diagram",
            get_streamlit_flow_state(),
            allow_new_edges=get_is_editable(),
            get_node_on_click=get_is_editable(),
            get_edge_on_click=get_is_editable(),
            enable_pane_menu=get_is_editable(),
            hide_watermark=True,
        ),
    )

    if get_is_editable():
        if get_streamlit_flow_state().selected_id is not None:
            set_streamlit_flow_selected_id(get_streamlit_flow_state().selected_id)
            get_streamlit_flow_state().selected_id = None  # type:ignore
            streamlit.rerun()

        with streamlit.sidebar:
            selected_id = get_streamlit_flow_selected_id()
            if selected_id is None:
                streamlit.title("Canvas Configuration")

                streamlit.button("Add Device", width=100, on_click=callback_button_add_device, args=(workcell,))

            else:
                if selected_id in get_assigned_device_dict():
                    assigned_device = get_assigned_device_dict()[selected_id]

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
