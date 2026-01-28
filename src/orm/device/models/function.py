from django.db import models

from .device import Device


class Function(models.Model):
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)

    execution_time_formula = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
