import streamlit
from utils import SessionStateManager, webapp_menu

streamlit.set_page_config(page_title="Home")

webapp_menu()

with SessionStateManager(SessionStateManager.key("static_flow_state")) as session_state_manager:
    pass

import streamlit as st
import streamlit_flow

handle_right_source = streamlit_flow.Handle("right", is_target=False)
handle_left_target = streamlit_flow.Handle("left", is_source=False)
handle_right_source.add_valid_targets(handle_left_target)

node_1 = streamlit_flow.MarkdownNode(
    pos_x=100,
    pos_y=100,
    content="Node 1",
    draggable=False,
    handles=[handle_right_source],
)

node_2 = streamlit_flow.MarkdownNode(
    pos_x=350,
    pos_y=50,
    content="Node 2",
    draggable=False,
    handles=[handle_right_source, handle_left_target],
)
node_3 = streamlit_flow.MarkdownNode(
    pos_x=350,
    pos_y=150,
    content="Node 3",
    draggable=False,
    handles=[handle_right_source, handle_left_target],
)
node_4 = streamlit_flow.MarkdownNode(
    pos_x=600,
    pos_y=100,
    content="Node 4",
    draggable=False,
    handles=[handle_left_target],
)
nodes: list[streamlit_flow.BaseNode] = [node_1, node_2, node_3, node_4]

marker_arrow = streamlit_flow.Marker("arrow")

edges = [
    streamlit_flow.Edge(
        node_1,
        handle_right_source,
        node_2,
        handle_left_target,
        animated=True,
        marker_end=marker_arrow,
    ),
    streamlit_flow.Edge(
        node_1,
        handle_right_source,
        node_3,
        handle_left_target,
        animated=True,
        marker_end=marker_arrow,
    ),
    streamlit_flow.Edge(
        node_2,
        handle_right_source,
        node_4,
        handle_left_target,
        animated=True,
        marker_end=marker_arrow,
    ),
    streamlit_flow.Edge(
        node_3,
        handle_right_source,
        node_4,
        handle_left_target,
        animated=True,
        marker_end=marker_arrow,
    ),
]

if "static_flow_state" not in st.session_state:
    st.session_state.static_flow_state = streamlit_flow.State(nodes, edges)

streamlit_flow.render(
    "static_flow",
    st.session_state.static_flow_state,
    fit_view=True,
    show_minimap=False,
    show_controls=False,
    pan_on_drag=False,
    allow_zoom=False,
)
