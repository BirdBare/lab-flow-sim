import streamlit

from orm.device.models import Function as _Function
from webapp.utils import SessionStateManager

KEY_PREFIX = "DEVICES_PAGE_STATE"


class TextInputDeviceFunctionExecutionTimeFormula(SessionStateManager.SessionStateItem[str]):
    @classmethod
    def get(cls, function: _Function) -> str:
        return streamlit.session_state[cls.key(function)]

    @classmethod
    def set(cls, value: str, function: _Function) -> None:
        streamlit.session_state[cls.key(function)] = value

    @classmethod
    def key(cls, function: _Function) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_text_input_device_function_{function.id}_execution_time_formula")


class TextInputDeviceComments(SessionStateManager.SessionStateItem[str]):
    @classmethod
    def get(cls, function: _Function) -> str:
        return streamlit.session_state[cls.key(function)]

    @classmethod
    def set(cls, value: str, function: _Function) -> None:
        streamlit.session_state[cls.key(function)] = value

    @classmethod
    def key(cls, function: _Function) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_text_input_device_function_{function.id}_comments")


class DeviceFunctions(SessionStateManager.SessionStateItem[list[_Function]]):
    @classmethod
    def get(cls) -> list[_Function]:
        if cls.key() not in streamlit.session_state:
            cls.set([])

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: list[_Function]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_device_function_list")
