from django.contrib import admin

from .models import AssignedDevice, DeviceConnection, Process, Workcell

admin.site.register(Workcell)
admin.site.register(AssignedDevice)
admin.site.register(DeviceConnection)
admin.site.register(Process)
