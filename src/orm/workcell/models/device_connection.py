from __future__ import annotations

import uuid

from django.db import models

from .assigned_device import AssignedDevice


class DeviceConnection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device_1 = models.ForeignKey(to=AssignedDevice, on_delete=models.CASCADE, related_name="+")
    device_2 = models.ForeignKey(to=AssignedDevice, on_delete=models.CASCADE, related_name="+")

    distance = models.PositiveIntegerField()
