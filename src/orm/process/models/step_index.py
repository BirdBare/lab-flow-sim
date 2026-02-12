import uuid

from django.db import models

from .steps import BaseStep


class StepIndex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    base_step = models.ForeignKey(to=BaseStep, on_delete=models.CASCADE)

    index = models.PositiveIntegerField()
