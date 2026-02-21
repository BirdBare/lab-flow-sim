import streamlit

from orm.workcell.models import Workcell as _Workcell
from webapp.utils import SessionStateManager

KEY_PREFIX = "WORKCELLS_PAGE_STATE"


class SelectboxWorkcell(SessionStateManager.SessionStateItem[_Workcell]):
    @classmethod
    def get(cls) -> _Workcell:
        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: _Workcell) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_workcell")
