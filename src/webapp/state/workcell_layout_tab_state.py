import streamlit
from streamlit_flow import StreamlitFlowState as _StreamlitFlowState

from orm.device.models import Device as _Device
from orm.workcell.models import AssignedDevice as _AssignedDevice
from orm.workcell.models import DeviceConnection as _DeviceConnection
from webapp.utils import SessionStateManager

KEY_PREFIX = "WORKCELLS_LAYOUT_TAB_STATE"


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


class StreamlitFlowSelectedID(SessionStateManager.SessionStateItem[str | None]):
    @classmethod
    def get(cls) -> str | None:
        return streamlit.session_state.get(cls.key(), None)

    @classmethod
    def set(cls, value: str | None) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_streamlit_flow_selected_id")


class AssignedDeviceDict(SessionStateManager.SessionStateItem[dict[str, _AssignedDevice]]):
    @classmethod
    def get(cls) -> dict[str, _AssignedDevice]:
        if cls.key() not in streamlit.session_state:
            cls.set({})

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: dict[str, _AssignedDevice]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_assigned_device_dict")


class DeviceConnectionDict(SessionStateManager.SessionStateItem[dict[str, _DeviceConnection]]):
    @classmethod
    def get(cls) -> dict[str, _DeviceConnection]:
        if cls.key() not in streamlit.session_state:
            cls.set({})

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: dict[str, _DeviceConnection]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_device__connection_dict")


class StreamlitFlowState(SessionStateManager.SessionStateItem[_StreamlitFlowState]):
    @classmethod
    def get(cls) -> _StreamlitFlowState:
        if cls.key() not in streamlit.session_state:
            cls.set(_StreamlitFlowState([], []))

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: _StreamlitFlowState) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_streamlit_flow_state")


class SelectboxDevice(SessionStateManager.SessionStateItem[_Device | None]):
    @classmethod
    def get(cls) -> _Device | None:
        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: _Device | None) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_device")
