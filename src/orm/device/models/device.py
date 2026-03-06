import uuid

from django.db import models


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)

    category = models.CharField(
        max_length=255,
        choices=(("Spatial", "Spatial"), ("Material", "Material")),
    )

    def __str__(self) -> str:
        return f"name={self.name} category={self.category}"
