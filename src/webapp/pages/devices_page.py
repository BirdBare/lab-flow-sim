import streamlit
from django.db.models.functions import Lower
from utils import SessionStateManager, webapp_menu

from orm.device.models import Device, Function
from webapp.state import devices_page_state as state

streamlit.set_page_config(page_title="Devices", layout="wide")

webapp_menu()


#
# CALLBACKS
#
def callback_button_edit_device_delete_function(index: int):
    state.DeviceFunctions.get().pop(index)


@streamlit.dialog("Device Editor", dismissible=False)
def edit_device(device: Device):

    with streamlit.container(gap=None):
        device.name = streamlit.text_input(
            "Device Name",
            value=device.name,
            key=f"{state.KEY_PREFIX}_device_editor_text_input_device_name",
        )

        #
        # Function Category
        #
        options = ["Material", "Spatial"]
        device.category = streamlit.selectbox(
            "Device Category",
            options,
            index=options.index(device.category),
            key=f"{state.KEY_PREFIX}_device_editor_selectbox_device_{device.id}_categorization",
            label_visibility="visible",
        )

        streamlit.divider()

        with streamlit.container(horizontal_alignment="center"):
            if streamlit.button("Add Function"):
                state.DeviceFunctions.get().insert(
                    0,
                    Function(device=device, name="New Function", execution_time_formula="0"),
                )

    for index, function in enumerate(state.DeviceFunctions.get()):
        with streamlit.expander(function.name):
            #
            # Function name
            #
            function.name = streamlit.text_input(
                "Function Name",
                value=function.name,
                key=f"{state.KEY_PREFIX}_device_editor_text_input_function_{function.id}_name",
            )

            #
            # Execution time formula
            #
            function.execution_time_formula = streamlit.text_input(
                "Execution Time Formula (s)",
                value=function.execution_time_formula,
                key=f"{state.KEY_PREFIX}_device_editor_text_input_function_{function.id}_execution_time_formula",
            )

            #
            # Comments
            #
            function.comments = streamlit.text_area(
                "Comments",
                value=function.comments,
                key=f"{state.KEY_PREFIX}_device_editor_text_input_function_{function.id}_comments",
            )

            with streamlit.container(horizontal_alignment="right"):
                streamlit.button(
                    "",
                    key=f"f{state.KEY_PREFIX}_device_editor_button_function_{function.id}_delete",
                    icon=":material/delete:",
                    type="tertiary",
                    on_click=callback_button_edit_device_delete_function,
                    args=(index,),
                )

    with streamlit.container(horizontal=True):
        if streamlit.button("Cancel", key=f"{state.KEY_PREFIX}_device_editor_button_cancel"):
            streamlit.rerun()

        if not device._state.adding:
            if streamlit.button("Delete", key=f"{state.KEY_PREFIX}_device_editor_button_delete"):
                device.delete()
                streamlit.rerun()

        if streamlit.button("Save", key=f"{state.KEY_PREFIX}_device_editor_button_save"):
            device.save()

            for function in Function.objects.filter(device=device).all():
                if function not in state.DeviceFunctions.get():
                    function.delete()

            for function in state.DeviceFunctions.get():
                function.save()

            streamlit.rerun()


with SessionStateManager() as session_state_manager:
    session_state_manager.add_persistent_keys(state.DeviceFunctions.key())

    streamlit.title("Devices")

    streamlit.text(
        "Devices can be added below. If a device has associated functions they will be listed. Click a device name to edit it.",
    )

    with streamlit.container(width=400):
        device_search_value = streamlit.text_input("Device Search", key=f"{state.KEY_PREFIX}_text_input_device_search")

    with streamlit.container(gap=None, horizontal_alignment="center"):
        streamlit.divider()
        if streamlit.button("New Device", key=f"{state.KEY_PREFIX}_button_new_device"):
            state.DeviceFunctions.set([])
            edit_device(Device(name="New Device", category="Material"))

    devices = list(Device.objects.filter(name__icontains=device_search_value).order_by(Lower("name")).all())
    device_chunks = [devices[i : i + 3] for i in range(0, len(devices), 3)]

    with streamlit.container(horizontal_alignment="center"):
        for device_chunk in device_chunks:
            columns = streamlit.columns(3, width=1000)
            for column_index, device in enumerate(device_chunk):
                with columns[column_index], streamlit.container(border=True):
                    with streamlit.container(gap=None, horizontal_alignment="center"):
                        streamlit.space()

                        #
                        # device name and edit button
                        #
                        if streamlit.button(
                            device.name,
                            type="tertiary",
                            key=f"{state.KEY_PREFIX}_button_device_{device.id}_edit",
                        ):
                            state.DeviceFunctions.set(
                                list(
                                    Function.objects.filter(device=device).order_by(Lower("name")).all(),
                                ),
                            )
                            edit_device(device)

                        #
                        # device category
                        #
                        streamlit.selectbox("Device Category", [device.category], disabled=True)

                        streamlit.divider()

                    for function in Function.objects.filter(device=device).order_by(Lower("name")).all():
                        with streamlit.expander(function.name):
                            #
                            # Execution Time
                            #
                            state.TextInputDeviceFunctionExecutionTimeFormula.set(
                                function.execution_time_formula,
                                function,
                            )
                            streamlit.text_input(
                                "Execution Time Formula (s)",
                                key=state.TextInputDeviceFunctionExecutionTimeFormula.key(function),
                                disabled=True,
                            )

                            #
                            # Comments
                            #
                            if function.comments.replace(" ", "").replace("\n", "") != "":
                                state.TextInputDeviceComments.set(function.comments, function)
                                streamlit.text_area(
                                    "Comments",
                                    key=state.TextInputDeviceComments.key(function),
                                    disabled=True,
                                )

                    streamlit.space()
