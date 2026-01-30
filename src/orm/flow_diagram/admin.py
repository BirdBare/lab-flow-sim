from django.contrib import admin
from .models import Node, AssignedDeviceNode

admin.site.register(Node)
admin.site.register(AssignedDeviceNode)