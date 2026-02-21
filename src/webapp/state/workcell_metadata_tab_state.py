import streamlit

from webapp.utils import SessionStateManager

KEY_PREFIX = "WORKCELL_METADATA_TAB_STATE"


class IsEditable(SessionStateManager.SessionStateItem[bool]):
    @classmethod
    def get(cls) -> bool:
        return streamlit.session_state.get(cls.key(), False)

    @classmethod
    def set(cls, value: bool) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_is_editable")


class TextInputWorkcellName(SessionStateManager.SessionStateItem[str]):
    @classmethod
    def get(cls) -> str:
        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: str) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_text_input_workcell_name")


class TextAreaWorkcellComments(SessionStateManager.SessionStateItem[str]):
    @classmethod
    def get(cls) -> str:
        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: str) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_text_area_workcell_comments")
