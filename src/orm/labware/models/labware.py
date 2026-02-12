import uuid

from django.db import models

from orm.workcell.models import Workcell


class Labware(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    workcell = models.ForeignKey(to=Workcell, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"name={self.name}"
