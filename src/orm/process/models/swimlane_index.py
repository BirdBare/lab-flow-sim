import uuid

from django.db import models

from .swimlane import Swimlane


class SwimlaneIndex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    swimlane = models.ForeignKey(to=Swimlane, on_delete=models.CASCADE)

    index = models.PositiveIntegerField()
