import streamlit

from orm.workcell_process.models import Process as _Process
from webapp.utils import SessionStateManager

KEY_PREFIX = "WORKCELL_PROCESSES_TAB_STATE"


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


class ForceUpdate(SessionStateManager.SessionStateItem[bool]):
    @classmethod
    def get(cls) -> bool:
        return streamlit.session_state.get(cls.key(), False)

    @classmethod
    def set(cls, value: bool) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_force_update")


class Processes(SessionStateManager.SessionStateItem[list[_Process]]):
    @classmethod
    def get(cls) -> list[_Process]:
        if cls.key() not in streamlit.session_state:
            cls.set([])

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: list[_Process]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_processes")


class SelectboxProcess(SessionStateManager.SessionStateItem[_Process | None]):
    @classmethod
    def get(cls) -> _Process | None:
        return streamlit.session_state.get(cls.key(), None)

    @classmethod
    def set(cls, value: _Process | None) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_process")
