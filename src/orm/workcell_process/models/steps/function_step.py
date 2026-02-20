from __future__ import annotations

from django.db import models

from orm.device.models import Function

from .base_step import BaseStep


class FunctionStep(BaseStep):
    function = models.ForeignKey(to=Function, on_delete=models.CASCADE)

    parallelization_key = models.CharField(max_length=255, blank=True)
