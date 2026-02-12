import streamlit
from utils import SessionStateManager, webapp_menu

streamlit.set_page_config(page_title="Labs", layout="wide")

webapp_menu()

with SessionStateManager() as session_state_manager:
    pass
