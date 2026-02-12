import streamlit


def webapp_menu():
    with streamlit.sidebar, streamlit.container(gap=None):
        with streamlit.container():
            streamlit.page_link("home.py", label="Home")
            streamlit.page_link("pages/devices.py", label="Devices")
            streamlit.page_link("pages/workcells.py", label="Workcells")
            streamlit.page_link("pages/labs.py", label="Labs")
            streamlit.page_link("pages/simulation.py", label="Simulation")
        streamlit.divider()
