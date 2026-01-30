from django.contrib import admin
from .models import Workcell,AssignedDevice,DeviceConnection

admin.site.register(Workcell)
admin.site.register(AssignedDevice)
admin.site.register(DeviceConnection)