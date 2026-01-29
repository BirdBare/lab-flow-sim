import uuid

from django.db import models

from orm.device.models import Device

from .workcell import Workcell


class AssignedDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    workcell = models.ForeignKey(to=Workcell, on_delete=models.CASCADE)

    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
