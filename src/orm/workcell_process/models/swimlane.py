import uuid

from django.db import models

from orm.workcell.models import Resource

from .process import Process


class Swimlane(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    process = models.ForeignKey(to=Process, on_delete=models.CASCADE)

    resource = models.ForeignKey(to=Resource, on_delete=models.CASCADE)

    multiplier_formula = models.CharField(max_length=255)
