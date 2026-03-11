import collections
import typing
import uuid

import streamlit
from streamlit_flow import Diagram as _StreamlitFlowDiagram
from streamlit_flow import Handle as _Handle

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


class HandleByDeviceCategoryByPosition(
    SessionStateManager.SessionStateItem[
        collections.defaultdict[
            typing.Literal["Material", "Spatial"],
            dict[typing.Literal["top", "bottom", "left", "right"], _Handle],
        ]
    ],
):
    @classmethod
    def get(
        cls,
    ) -> collections.defaultdict[
        typing.Literal["Material", "Spatial"],
        dict[typing.Literal["top", "bottom", "left", "right"], _Handle],
    ]:
        if cls.key() not in streamlit.session_state:
            cls.set(collections.defaultdict(dict))

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(
        cls,
        value: collections.defaultdict[
            typing.Literal["Material", "Spatial"],
            dict[typing.Literal["top", "bottom", "left", "right"], _Handle],
        ],
    ) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_handle_by_device_category_by_position")


class MaterialNodeIDs(SessionStateManager.SessionStateItem[list[uuid.UUID]]):
    @classmethod
    def get(cls) -> list[uuid.UUID]:
        if cls.key() not in streamlit.session_state:
            cls.set([])

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: list[uuid.UUID]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_material_node_ids")


class SpatialNodeIDs(SessionStateManager.SessionStateItem[list[uuid.UUID]]):
    @classmethod
    def get(cls) -> list[uuid.UUID]:
        if cls.key() not in streamlit.session_state:
            cls.set([])

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: list[uuid.UUID]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_spatial_node_ids")


class StreamlitFlowDiagram(SessionStateManager.SessionStateItem[_StreamlitFlowDiagram]):
    @classmethod
    def get(cls) -> _StreamlitFlowDiagram:
        if cls.key() not in streamlit.session_state:
            cls.set(_StreamlitFlowDiagram([], [], [], []))

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: _StreamlitFlowDiagram) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_streamlit_flow_state")


class StreamlitFlowSelectedID(SessionStateManager.SessionStateItem[uuid.UUID | None]):
    @classmethod
    def get(cls) -> uuid.UUID | None:
        return streamlit.session_state.get(cls.key(), None)

    @classmethod
    def set(cls, value: uuid.UUID | None) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_streamlit_flow_selected_id")


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


class AssignedDeviceByNodeID(SessionStateManager.SessionStateItem[dict[uuid.UUID, _AssignedDevice]]):
    @classmethod
    def get(cls) -> dict[uuid.UUID, _AssignedDevice]:
        if cls.key() not in streamlit.session_state:
            cls.set({})

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: dict[uuid.UUID, _AssignedDevice]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_assigned_device_by_node_id")


class DeviceConnectionByEdgeID(SessionStateManager.SessionStateItem[dict[uuid.UUID, _DeviceConnection]]):
    @classmethod
    def get(cls) -> dict[uuid.UUID, _DeviceConnection]:
        if cls.key() not in streamlit.session_state:
            cls.set({})

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: dict[uuid.UUID, _DeviceConnection]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_device_connection_by_edge_id")


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
