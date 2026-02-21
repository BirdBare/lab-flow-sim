import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager

import webapp.state.workcell_process_swimlanes_tab_state as state
from orm.device.models import Function
from orm.workcell.models import Labware
from orm.workcell_process.models import FunctionStep, Process, ProcessStep, StepIndex, Swimlane, SwimlaneIndex


#
# BUTTON CALLBACKS
#
def callback_button_add_swimlane(process: Process):
    # set both as none. Will be updated if process is saved.
    swimlane = Swimlane(process=process, labware=None, multiplier_formula="")

    # add
    state.get_swimlanes().append(swimlane)

    # Set initial values for new swimlane
    state.set_selectbox_swimlane_labware(swimlane, None)
    state.set_text_input_swimlane_multiplier(swimlane, "")


def callback_button_move_swimlane_left(swimlane: Swimlane):
    index = state.get_swimlanes().index(swimlane)

    state.get_swimlanes().remove(swimlane)

    # When moving left the insert position can suddenly be less than zero.
    state.get_swimlanes().insert(max(index - 1, 0), swimlane)


def callback_button_move_swimlane_right(swimlane: Swimlane):
    index = state.get_swimlanes().index(swimlane)

    state.get_swimlanes().remove(swimlane)

    state.get_swimlanes().insert(index + 1, swimlane)


def callback_button_delete_swimlane(swimlane: Swimlane):
    state.get_swimlanes().remove(swimlane)
    del state.get_swimlane_steps_dict()[swimlane]


def callback_button_swimlane_add_function_step(swimlane: Swimlane, insert_index: int):
    step = FunctionStep(swimlane=swimlane, function=None, parallelization_key="")

    state.get_swimlane_steps_dict()[swimlane].insert(insert_index, step)

    state.set_selectbox_step_function(step, None)
    state.set_selectbox_step_parallelization(step, None)


def callback_button_swimlane_add_process_step(swimlane: Swimlane, insert_index: int):
    step = ProcessStep(swimlane=swimlane, process=None, connected_swimlane=None)

    state.get_swimlane_steps_dict()[swimlane].insert(insert_index, step)

    state.set_selectbox_step_process(step, None)
    state.set_selectbox_step_swimlane(step, None)


def callback_button_delete_step(swimlane: Swimlane, step: FunctionStep | ProcessStep):
    state.get_swimlane_steps_dict()[swimlane].remove(step)


#
# TAB
#
def render_tab(
    session_state_manager: SessionStateManager,
    process: Process,
    is_editable: bool,
    force_update: bool,
):
    if is_editable:
        with streamlit.container(horizontal_alignment="center"):
            streamlit.button(
                "Add Swimlane",
                key=f"button_{state._KEY_PREFIX}_add_swimlane",
                on_click=callback_button_add_swimlane,
                args=(process,),
            )

    session_state_manager.add_persistent_keys(state.get_swimlanes_key())
    session_state_manager.add_persistent_keys(state.get_swimlane_steps_dict_key())
    if not is_editable or force_update:
        state.reset_swimlanes()
        state.reset_swimlane_steps_dict()

        for swimlane_index in SwimlaneIndex.objects.filter(swimlane__process=process).order_by("index").all():
            swimlane = swimlane_index.swimlane
            state.get_swimlanes().append(swimlane)

            for step_index in StepIndex.objects.filter(base_step__swimlane=swimlane).order_by("index").all():
                step = step_index.base_step.cast()

                state.get_swimlane_steps_dict()[swimlane].append(step)

    global_parallelization_keys = {
        step.parallelization_key
        for steps in state.get_swimlane_steps_dict().values()
        for step in steps
        if isinstance(step, FunctionStep) and step.parallelization_key is not None and step.parallelization_key != ""
    }

    swimlanes = state.get_swimlanes()

    swimlane_chunks = [swimlanes[i : i + 3] for i in range(0, len(swimlanes), 3)]

    tabs = streamlit.tabs([f"Page {i + 1}" for i in range(max(len(swimlane_chunks), 1))])

    for swimlane_chunk_index, swimlane_chunk in enumerate(swimlane_chunks):
        with tabs[swimlane_chunk_index], streamlit.container(horizontal=True, horizontal_alignment="center"):
            columns = streamlit.columns(3)

            #
            # Render Swimlanes
            #
            for swimlane_index, swimlane in enumerate(swimlane_chunk):
                swimlane_parallelization_keys = {
                    step.parallelization_key
                    for step in state.get_swimlane_steps_dict()[swimlane]
                    if isinstance(step, FunctionStep)
                    and step.parallelization_key is not None
                    and step.parallelization_key != ""
                }
                with columns[swimlane_index], streamlit.container(border=True, gap=None):
                    with streamlit.container():
                        with streamlit.container(
                            horizontal=True,
                            horizontal_alignment="center",
                            vertical_alignment="center",
                        ):
                            #
                            # Swimlane Move Left Button
                            #
                            if is_editable:
                                streamlit.button(
                                    "",
                                    icon=":material/arrow_back_ios:",
                                    type="tertiary",
                                    help="Move Swimlane left",
                                    key=f"{state._KEY_PREFIX}_button_move_swimlane_{swimlane.id}_left",
                                    on_click=callback_button_move_swimlane_left,
                                    args=(swimlane,),
                                )

                            #
                            # Swimlane Labware Selectbox
                            #
                            session_state_manager.add_persistent_keys(
                                state.get_selectbox_swimlane_labware_key(swimlane),
                            )
                            if not is_editable or force_update:
                                state.set_selectbox_swimlane_labware(swimlane, swimlane.labware)

                            swimlane.labware = streamlit.selectbox(
                                "Labware",
                                Labware.objects.filter(workcell=process.workcell).order_by(Lower("name")).all(),
                                format_func=lambda x: x.name,
                                key=state.get_selectbox_swimlane_labware_key(swimlane),
                                disabled=not is_editable,
                            )

                            #
                            # Swimlane Move Right Button
                            #
                            if is_editable is True:
                                streamlit.button(
                                    "",
                                    icon=":material/arrow_forward_ios:",
                                    type="tertiary",
                                    help="Move Swimlane right",
                                    key=f"{state._KEY_PREFIX}_button_move_swimlane_{swimlane.id}__right",
                                    on_click=callback_button_move_swimlane_right,
                                    args=(swimlane,),
                                )

                        #
                        # Swimlane Multiplier formula
                        #
                        session_state_manager.add_persistent_keys(
                            state.get_text_input_swimlane_multiplier_key(swimlane)
                        )
                        if not is_editable or force_update:
                            state.set_text_input_swimlane_multiplier(swimlane, swimlane.multiplier_formula)

                        swimlane.multiplier_formula = streamlit.text_input(
                            "Multiplier Formula",
                            help="Creates multiples of this swimlane for modelling dependent on the formula. May be parameterized with captialized X.",
                            key=state.get_text_input_swimlane_multiplier_key(swimlane),
                            disabled=not is_editable,
                        )

                    #
                    # Swimlane delete
                    #
                    with streamlit.container(
                        horizontal=True,
                        horizontal_alignment="right",
                    ):
                        if is_editable is True:
                            streamlit.button(
                                "",
                                icon=":material/delete:",
                                type="tertiary",
                                help="Delete swimlane",
                                key=f"{state._KEY_PREFIX}_button_swimlane_{swimlane.id}_delete",
                                on_click=callback_button_delete_swimlane,
                                args=(swimlane,),
                            )

                    streamlit.divider()

                    #
                    # New step buttons
                    #
                    if is_editable:
                        with streamlit.container(horizontal=True, horizontal_alignment="center"):
                            streamlit.button(
                                "",
                                icon=":material/developer_board:",
                                type="tertiary",
                                help="Add Device Function",
                                key=f"{state._KEY_PREFIX}_button_swimlane_{swimlane.id}_add_function_step_0",
                                on_click=callback_button_swimlane_add_function_step,
                                args=(swimlane, 0),
                            )
                            streamlit.button(
                                "",
                                icon=":material/account_tree:",
                                type="tertiary",
                                help="Add Process",
                                key=f"{state._KEY_PREFIX}_button_swimlane_{swimlane.id}_add_process_step_0",
                                on_click=callback_button_swimlane_add_process_step,
                                args=(swimlane, 0),
                            )

                    #
                    # Render Steps
                    #
                    for step_index, step in enumerate(state.get_swimlane_steps_dict()[swimlane]):
                        with streamlit.container(border=True, gap=None):
                            with streamlit.container():
                                #
                                # Function Step
                                #
                                if isinstance(step, FunctionStep):
                                    #
                                    # Step Function
                                    #
                                    session_state_manager.add_persistent_keys(
                                        state.get_selectbox_step_function_key(step)
                                    )
                                    if not is_editable or force_update:
                                        state.set_selectbox_step_function(step, step.function)

                                    step.function = streamlit.selectbox(
                                        "Device Function",
                                        sorted(
                                            Function.objects.all(),
                                            key=lambda x: f"{x.device.name}: {x.name}".lower(),
                                        ),
                                        key=state.get_selectbox_step_function_key(step),
                                        disabled=not is_editable,
                                        format_func=lambda x: f"{x.device.name}: {x.name}",
                                    )

                                    #
                                    # Step Parallelization Key
                                    #
                                    session_state_manager.add_persistent_keys(
                                        state.get_selectbox_step_parallelization_key(step),
                                    )
                                    if not is_editable or force_update:
                                        state.set_selectbox_step_parallelization(step, step.parallelization_key)

                                    paralellization_key = streamlit.selectbox(
                                        "Function Parallelization Key",
                                        {
                                            key
                                            for key in global_parallelization_keys
                                            if key not in swimlane_parallelization_keys
                                        },
                                        index=None,
                                        key=state.get_selectbox_step_parallelization_key(step),
                                        disabled=not is_editable,
                                        accept_new_options=True,
                                    )
                                    if paralellization_key is None:
                                        paralellization_key = ""
                                    step.parallelization_key = paralellization_key

                                #
                                # Process Step
                                #
                                else:
                                    #
                                    # Step Process
                                    #
                                    session_state_manager.add_persistent_keys(
                                        state.get_selectbox_step_process_key(step)
                                    )
                                    if not is_editable or force_update:
                                        state.set_selectbox_step_process(step, step.process)

                                    step_process = step.process = streamlit.selectbox(
                                        "Process",
                                        Process.objects.filter(workcell=process.workcell)
                                        .exclude(id=process.id)
                                        .order_by(Lower("name"))
                                        .all(),
                                        key=state.get_selectbox_step_process_key(step),
                                        disabled=not is_editable,
                                        format_func=lambda x: x.name,
                                    )
                                    #
                                    # Step Connected Swimlane
                                    #
                                    session_state_manager.add_persistent_keys(
                                        state.get_selectbox_step_swimlane_key(step)
                                    )
                                    if not is_editable or force_update:
                                        state.set_selectbox_step_swimlane(step, step.connected_swimlane)

                                    step.connected_swimlane = streamlit.selectbox(
                                        "Connected Swimlane",
                                        []
                                        if step_process is None
                                        else Swimlane.objects.filter(
                                            process=step_process,
                                        ).all(),
                                        format_func=lambda x: x.name,
                                        key=state.get_selectbox_step_swimlane_key(step),
                                        disabled=not is_editable,
                                    )

                            #
                            # Step delete
                            #
                            with streamlit.container(
                                horizontal=True,
                                horizontal_alignment="right",
                            ):
                                if is_editable is True:
                                    streamlit.button(
                                        "",
                                        icon=":material/delete:",
                                        type="tertiary",
                                        help="Delete swimlane",
                                        key=f"{state._KEY_PREFIX}_button_step_{step.id}_delete",
                                        on_click=callback_button_delete_step,
                                        args=(swimlane, step),
                                    )

                        #
                        # New step buttons
                        #
                        if is_editable:
                            with streamlit.container(horizontal=True, horizontal_alignment="center"):
                                streamlit.button(
                                    "",
                                    icon=":material/developer_board:",
                                    type="tertiary",
                                    help="Add Device Function",
                                    key=f"{state._KEY_PREFIX}_button_swimlane_{swimlane.id}_add_function_step_{step_index + 1}",
                                    on_click=callback_button_swimlane_add_function_step,
                                    args=(swimlane, step_index + 1),
                                )
                                streamlit.button(
                                    "",
                                    icon=":material/account_tree:",
                                    type="tertiary",
                                    help="Add Process",
                                    key=f"{state._KEY_PREFIX}_button_swimlane_{swimlane.id}_add_process_step_{step_index + 1}",
                                    on_click=callback_button_swimlane_add_process_step,
                                    args=(swimlane, step_index + 1),
                                )
