import streamlit
from utils import SessionStateManager, webapp_menu
from orm.device.models import Device, Function
import uuid
from django.db.models.functions import Lower
streamlit.set_page_config(page_title="Devices",layout="wide")

webapp_menu()

@streamlit.dialog("Device Editor",dismissible=False)
def edit_device(device:Device):
    functions:list[Function] = streamlit.session_state["edit_device_functions"]

    with streamlit.container(gap=None):
        device.name = streamlit.text_input(
            "Device Name",
            value=device.name,
            key=f"device_{device.id}_name")

        streamlit.divider()

        with streamlit.container(horizontal_alignment="center"):
            if streamlit.button("Add Function"):
                functions.insert(0,Function(device=device,name="New Function",category="Material",execution_time_formula="0"))
    
    for index, function in enumerate(functions):
        with streamlit.container(border=True):
            function.name = streamlit.text_input(
                "Function Name",
                value=function.name,
                key=f"function_{function.id}_name"
            )

            function.category = streamlit.selectbox(
                "Categorization",
                ["Material","Spatial"],
                key=f"function_{function.id}_categorization",label_visibility="visible")

            function.execution_time_formula = streamlit.text_input(
                "Execution Time Formula (s)",
                value=function.execution_time_formula,
                key=f"function_{function.id}_execution_time_formula"
            )

            with streamlit.container(horizontal_alignment="right"):
                streamlit.button(
                    "",
                    key=f"function_{function.id}_delete",
                    icon=":material/delete:",
                    type="tertiary",
                    on_click=lambda index: streamlit.session_state["edit_device_functions"].pop(index),
                    args=(index,)
                )

    with streamlit.container(horizontal=True):
        if streamlit.button("Cancel"):
            streamlit.rerun()

        if not device._state.adding:
            if streamlit.button("Delete"):
                device.delete()
                streamlit.rerun()
        
        if streamlit.button("Save"):
            device.save()

            for function in functions:
                function.save()

            streamlit.rerun()


with SessionStateManager("edit_device_functions") as session_state_manager:
    streamlit.title("Devices")

    streamlit.text("Devices can be added below. If a device has associated functions they will be listed. Click a device name to edit it.")
    
    with streamlit.container(width=400):
        device_search_value = streamlit.text_input("Device Search")

    with streamlit.container(gap=None,horizontal_alignment="center"):
        streamlit.divider()
        if streamlit.button("New Device"):
            streamlit.session_state["edit_device_functions"] = []
            edit_device(Device(name="New Device"))
            
    devices = list(Device.objects.filter(name__icontains=device_search_value).order_by(Lower("name")).all())
    device_chunks = [devices[i:i + 3] for i in range(0, len(devices), 3)]

    with streamlit.container(horizontal_alignment="center"):
        for device_chunk in device_chunks:
            columns = streamlit.columns(3,width=1000)
            for column_index, device in enumerate(device_chunk):
                with columns[column_index], streamlit.container(border=True):
                    with streamlit.container(gap=None,horizontal_alignment="center"):
                        streamlit.space()

                        if streamlit.button(device.name, type="tertiary",key=f"device_{device.id}_edit"):
                            streamlit.session_state["edit_device_functions"] = list(Function.objects.filter(device=device).order_by(Lower("name")).all())
                            edit_device(device)
    
                        streamlit.divider()
                    
                    for function in Function.objects.filter(device=device).order_by(Lower("name")).all():
                        with streamlit.expander(function.name):
                            streamlit.selectbox(
                                "Categorization",
                                [function.category],
                                key=f"device_function_{function.id}_categorization",
                                disabled=True
                                )
                            
                            streamlit.text_input(
                                "Execution Time Formula",
                                function.execution_time_formula,
                                key=f"device_function_{function.id}_execution_time_formula",
                                disabled=True
                                )
                            
                    with streamlit.container(horizontal_alignment="right"):
                        streamlit.button(
                            "",
                            key=f"device_{device.id}_delete",
                            icon=":material/delete:",
                            type="tertiary",
                            on_click=lambda device: device.delete(),
                            args=(device,)
                        )
                    streamlit.space()
