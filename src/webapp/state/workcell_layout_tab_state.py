import streamlit
from streamlit_flow import BaseNode as _BaseNode
from streamlit_flow import Edge as _Edge
from streamlit_flow import State as _StreamlitFlowState

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


class StreamlitFlowSelected(SessionStateManager.SessionStateItem[_BaseNode | _Edge | None]):
    @classmethod
    def get(cls) -> _BaseNode | _Edge | None:
        return streamlit.session_state.get(cls.key(), None)

    @classmethod
    def set(cls, value: _BaseNode | _Edge | None) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_streamlit_flow_selected")


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


class AssignedDeviceByNodeID(SessionStateManager.SessionStateItem[dict[str, _AssignedDevice]]):
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


class DeviceConnectionByEdgeID(SessionStateManager.SessionStateItem[dict[str, _DeviceConnection]]):
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


class SelectboxAssignedDeviceDevice(SessionStateManager.SessionStateItem[_Device | None]):
    @classmethod
    def get(cls) -> _Device | None:
        return streamlit.session_state.get(cls.key(), None)

    @classmethod
    def set(cls, value: _Device | None) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_assigned_device_device")


class NumberInputDeviceConnectionDistance(SessionStateManager.SessionStateItem[int]):
    @classmethod
    def get(cls) -> int:
        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: int) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_number_input_device_connnection_distance")
