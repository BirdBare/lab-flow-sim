import streamlit


def webapp_menu():
    with streamlit.sidebar, streamlit.container(gap=None):
        with streamlit.container():
            streamlit.page_link("home.py", label="Home")
            streamlit.page_link("pages/devices_page.py", label="Devices")
            streamlit.page_link("pages/workcells_page.py", label="Workcells")
            streamlit.page_link("pages/labs_page.py", label="Labs")
            streamlit.page_link("pages/simulation_page.py", label="Simulation")
        streamlit.divider()
