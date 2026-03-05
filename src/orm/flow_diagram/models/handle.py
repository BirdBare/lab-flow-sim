from __future__ import annotations

import uuid

from django.db import models


class Handle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    position = models.CharField(
        max_length=10,
        choices=(("top", "top"), ("bottom", "bottom"), ("left", "left"), ("right", "right")),
    )
    is_source = models.BooleanField()
    is_target = models.BooleanField()

    valid_targets: models.ManyToManyField[Handle, Handle] = models.ManyToManyField(to="self")

    def __str__(self):
        return f"position={self.position}, is_source={self.is_source}, is_target={self.is_target}"
