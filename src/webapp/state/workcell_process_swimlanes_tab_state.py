import collections

import streamlit

from orm.device.models import Function
from orm.workcell.models import Labware
from orm.workcell_process.models import FunctionStep, Process, ProcessStep, Swimlane

_KEY_PREFIX = "workcell_process_swimlanes"


#
# SWIMLANE STEPS
#
def get_swimlanes_key() -> str:
    return f"{_KEY_PREFIX}_swimlanes"


def get_swimlanes() -> list[Swimlane]:
    if get_swimlanes_key() not in streamlit.session_state:
        reset_swimlanes()

    return streamlit.session_state[get_swimlanes_key()]


def reset_swimlanes():
    streamlit.session_state[get_swimlanes_key()] = []


#
# SWIMLANE STEPS
#
def get_swimlane_steps_dict_key() -> str:
    return f"{_KEY_PREFIX}_swimlane_steps_dict"


def get_swimlane_steps_dict() -> dict[Swimlane, list[FunctionStep | ProcessStep]]:
    if get_swimlane_steps_dict_key() not in streamlit.session_state:
        reset_swimlane_steps_dict()

    return streamlit.session_state[get_swimlane_steps_dict_key()]


def reset_swimlane_steps_dict():
    streamlit.session_state[get_swimlane_steps_dict_key()] = collections.defaultdict(list)


#
# SELECTBOX SWIMLANE LABWARE
#
def get_selectbox_swimlane_labware_key(swimlane: Swimlane) -> str:
    return f"{_KEY_PREFIX}_selectbox_swimlane_{swimlane.id}_labware"


def set_selectbox_swimlane_labware(swimlane: Swimlane, value: Labware | None):
    streamlit.session_state[get_selectbox_swimlane_labware_key(swimlane)] = value


#
# TEXT INPUT MULTIPLIER
#
def get_text_input_swimlane_multiplier_key(swimlane: Swimlane) -> str:
    return f"{_KEY_PREFIX}_text_input_swimlane_{swimlane.id}_multiplier"


def set_text_input_swimlane_multiplier(swimlane: Swimlane, value: str):
    streamlit.session_state[get_text_input_swimlane_multiplier_key(swimlane)] = value


#
# SELECTBOX STEP FUNCTION
#
def get_selectbox_step_function_key(step: FunctionStep) -> str:
    return f"{_KEY_PREFIX}_selectbox_step_{step.id}_function"


def set_selectbox_step_function(step: FunctionStep, value: Function | None):
    streamlit.session_state[get_selectbox_step_function_key(step)] = value


#
# SELECTBOX STEP PARALLELIZATION
#
def get_selectbox_step_parallelization_key(step: FunctionStep) -> str:
    return f"{_KEY_PREFIX}_selectbox_step_{step.id}_parallelization"


def set_selectbox_step_parallelization(step: FunctionStep, value: str | None):
    streamlit.session_state[get_selectbox_step_parallelization_key(step)] = value


#
# SELECTBOX STEP PROCESS
#
def get_selectbox_step_process_key(step: ProcessStep) -> str:
    return f"{_KEY_PREFIX}_selectbox_step_{step.id}_process"


def set_selectbox_step_process(step: ProcessStep, value: Process | None):
    streamlit.session_state[get_selectbox_step_process_key(step)] = value


#
# SELECTBOX STEP SWIMLANE
#
def get_selectbox_step_swimlane_key(step: ProcessStep) -> str:
    return f"{_KEY_PREFIX}_selectbox_step_{step.id}_swimlane"


def set_selectbox_step_swimlane(step: ProcessStep, value: Swimlane | None):
    streamlit.session_state[get_selectbox_step_swimlane_key(step)] = value
