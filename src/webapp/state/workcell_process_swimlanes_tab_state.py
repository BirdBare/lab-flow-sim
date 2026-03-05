import collections as _collections

import streamlit

from orm.device.models import Function as _Function
from orm.workcell.models import Resource as _Resource
from orm.workcell_process.models import FunctionStep as _FunctionStep
from orm.workcell_process.models import Process as _Process
from orm.workcell_process.models import ProcessStep as _ProcessStep
from orm.workcell_process.models import Swimlane as _Swimlane
from webapp.utils import SessionStateManager

KEY_PREFIX = "workcell_process_swimlanes"


class Swimlanes(SessionStateManager.SessionStateItem[list[_Swimlane]]):
    @classmethod
    def get(cls) -> list[_Swimlane]:
        if cls.key() not in streamlit.session_state:
            cls.set([])

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: list[_Swimlane]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_swimlane_list")


class SwimlaneStepsBySwimlane(
    SessionStateManager.SessionStateItem[_collections.defaultdict[_Swimlane, list[_FunctionStep | _ProcessStep]]],
):
    @classmethod
    def get(cls) -> _collections.defaultdict[_Swimlane, list[_FunctionStep | _ProcessStep]]:
        if cls.key() not in streamlit.session_state:
            cls.set(_collections.defaultdict(list))

        return streamlit.session_state[cls.key()]

    @classmethod
    def set(cls, value: _collections.defaultdict[_Swimlane, list[_FunctionStep | _ProcessStep]]) -> None:
        streamlit.session_state[cls.key()] = value

    @classmethod
    def key(cls) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_swimlane_steps_dict")


class SelectboxSwimlaneResource(SessionStateManager.SessionStateItem[_Resource | None]):
    @classmethod
    def get(cls, swimlane: _Swimlane) -> _Resource | None:
        return streamlit.session_state[cls.key(swimlane)]

    @classmethod
    def set(cls, value: _Resource | None, swimlane: _Swimlane) -> None:
        streamlit.session_state[cls.key(swimlane)] = value

    @classmethod
    def key(cls, swimlane: _Swimlane) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_swimlane_{swimlane.id}_resource")


class TextInputSwimlaneMultiplier(SessionStateManager.SessionStateItem[str]):
    @classmethod
    def get(cls, swimlane: _Swimlane) -> str:
        return streamlit.session_state[cls.key(swimlane)]

    @classmethod
    def set(cls, value: str, swimlane: _Swimlane) -> None:
        streamlit.session_state[cls.key(swimlane)] = value

    @classmethod
    def key(cls, swimlane: _Swimlane) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_swimlane_{swimlane.id}_multiplier")


class SelectboxStepFunction(SessionStateManager.SessionStateItem[_Function | None]):
    @classmethod
    def get(cls, step: _FunctionStep) -> _Function | None:
        return streamlit.session_state[cls.key(step)]

    @classmethod
    def set(cls, value: _Function | None, step: _FunctionStep) -> None:
        streamlit.session_state[cls.key(step)] = value

    @classmethod
    def key(cls, step: _FunctionStep) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_step_{step.id}_function")


class SelectboxStepParallelization(SessionStateManager.SessionStateItem[str | None]):
    @classmethod
    def get(cls, step: _FunctionStep) -> str | None:
        return streamlit.session_state[cls.key(step)]

    @classmethod
    def set(cls, value: str | None, step: _FunctionStep) -> None:
        streamlit.session_state[cls.key(step)] = value

    @classmethod
    def key(cls, step: _FunctionStep) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_step_{step.id}_parallelization")


class SelectboxStepProcess(SessionStateManager.SessionStateItem[_Process | None]):
    @classmethod
    def get(cls, step: _ProcessStep) -> _Process | None:
        return streamlit.session_state[cls.key(step)]

    @classmethod
    def set(cls, value: _Process | None, step: _ProcessStep) -> None:
        streamlit.session_state[cls.key(step)] = value

    @classmethod
    def key(cls, step: _ProcessStep) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_step_{step.id}_process")


class SelectboxStepSwimlane(SessionStateManager.SessionStateItem[_Swimlane | None]):
    @classmethod
    def get(cls, step: _ProcessStep) -> _Swimlane | None:
        return streamlit.session_state[cls.key(step)]

    @classmethod
    def set(cls, value: _Swimlane | None, step: _ProcessStep) -> None:
        streamlit.session_state[cls.key(step)] = value

    @classmethod
    def key(cls, step: _ProcessStep) -> SessionStateManager.key:
        return SessionStateManager.key(f"{KEY_PREFIX}_selectbox_step_{step.id}_swimlane")
