from __future__ import annotations

import uuid

from django.db import models

from .assigned_device import AssignedDevice

class DeviceConnection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assigned_devices:models.ManyToManyField[AssignedDevice,DeviceConnection] = models.ManyToManyField(to=AssignedDevice)

    distance = models.PositiveIntegerField()