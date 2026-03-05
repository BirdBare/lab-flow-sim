from __future__ import annotations

import uuid

from django.db import models

from .handle import Handle
from .node import Node


class Edge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    source_node = models.ForeignKey(to=Node, on_delete=models.CASCADE, related_name="+")
    source_handle = models.ForeignKey(to=Handle, on_delete=models.CASCADE, related_name="+")
    target_node = models.ForeignKey(to=Node, on_delete=models.CASCADE, related_name="+")
    target_handle = models.ForeignKey(to=Handle, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return f"source_node={self.source_node} source_handle={self.source_handle} target_node={self.target_node} target_handle={self.target_handle}"
