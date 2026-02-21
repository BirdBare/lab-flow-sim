import streamlit

from webapp.utils import SessionStateManager

KEY_PREFIX = "WORKCELL_PROCESS_METADATA_TAB_STATE"


class TextInputProcessName(SessionStateManager.SessionStateItem[str]):
    @classmethod
    def get(cls) -> str:
        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: str) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_text_input_process_name")


class TextAreaProcessComments(SessionStateManager.SessionStateItem[str]):
    @classmethod
    def get(cls) -> str:
        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: str) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_text_area_process_comments")
