from utils import SessionStateManager
from orm.workcell.models import Workcell, AssignedDevice, DeviceConnection
from orm.flow_diagram.models import AssignedDeviceNode
from streamlit_flow import streamlit_flow,StreamlitFlowNode,StreamlitFlowEdge,StreamlitFlowState
import streamlit

def render_workcell_diagram_tab(session_state_manager: SessionStateManager, workcell_is_editable: bool, workcell:Workcell):

    session_state_manager.add_persistent_keys("workcell_streamlit_flow_state")
    if "workcell_streamlit_flow_state" not in streamlit.session_state:
        nodes:list[StreamlitFlowNode] = []
        edges:list[StreamlitFlowEdge] = []

        assigned_devices = AssignedDevice.objects.filter(workcell=workcell).all()

        for assigned_device in assigned_devices:
            db_node = AssignedDeviceNode.objects.filter(assigned_device=assigned_device).get().node

            node = StreamlitFlowNode(str(db_node.id),(db_node.x_pos,db_node.y_pos),{"content":assigned_device.device.name})

            nodes.append(node)

        for device_connection in DeviceConnection.objects.filter(assigned_devices__in=assigned_devices).distinct().all():
            connected_devices = list(device_connection.assigned_devices.all())

            device_1 = connected_devices[0]
            db_node_1 = AssignedDeviceNode.objects.filter(assigned_device=device_1).get().node

            device_2 = connected_devices[1]
            db_node_2 = AssignedDeviceNode.objects.filter(assigned_device=device_2).get().node

            edge = StreamlitFlowEdge(f"{db_node_1.id}-{db_node_2.id}",str(db_node_1.id),str(db_node_2.id))

            edges.append(edge)

        streamlit.session_state["workcell_streamlit_flow_state"] = StreamlitFlowState(nodes,edges)
    
    streamlit.session_state["workcell_streamlit_flow_state"] = streamlit_flow("workcell_device_diagram",streamlit.session_state["workcell_streamlit_flow_state"],get_node_on_click=True,get_edge_on_click=True)
    
    streamlit_flow_state: StreamlitFlowState = streamlit.session_state["workcell_streamlit_flow_state"]

    with streamlit.sidebar:
        streamlit.text(streamlit_flow_state.selected_id)