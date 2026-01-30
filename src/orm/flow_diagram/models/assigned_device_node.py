import uuid

from django.db import models
from .node import Node
from orm.workcell.models import AssignedDevice

class AssignedDeviceNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assigned_device = models.ForeignKey(to=AssignedDevice,on_delete=models.CASCADE)
    node = models.ForeignKey(to=Node,on_delete=models.CASCADE)

    def __str__(self):
        return f"assigned_device=[{self.assigned_device}] node=[{self.node}]"