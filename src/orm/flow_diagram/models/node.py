import uuid

from django.db import models


class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    x_pos = models.PositiveIntegerField()
    y_pos = models.PositiveIntegerField()
