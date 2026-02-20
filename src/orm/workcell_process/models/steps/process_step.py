from __future__ import annotations

from django.db import models

from ..process import Process
from ..swimlane import Swimlane
from .base_step import BaseStep


class ProcessStep(BaseStep):
    process = models.ForeignKey(to=Process, on_delete=models.CASCADE)

    connected_swimlane = models.ForeignKey(
        to=Swimlane,
        on_delete=models.CASCADE,
    )
