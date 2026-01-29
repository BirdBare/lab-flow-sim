import streamlit
from utils import SessionStateManager, webapp_menu

streamlit.set_page_config(page_title="Workcells", layout="wide")

webapp_menu()

with SessionStateManager() as session_state_manager:
    streamlit.title("Workcells")

    streamlit.text(
        "Workcells can be created here. Once a workcell is created with its associated devices you can create processes.",
    )

    with streamlit.container(gap=None, horizontal_alignment="center"):
        streamlit.divider()
        if streamlit.button("New Device"):
            streamlit.session_state["edit_device_functions"] = []
            edit_device(Device(name="New Device"))
