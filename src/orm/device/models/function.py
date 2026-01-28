from django.db import models

from .device import Device
import uuid

class Function(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)

    category = models.CharField(max_length=255,choices=(("Spatial","Spatial"),("Material","Material"),("Informational","Informational")))

    execution_time_formula = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
