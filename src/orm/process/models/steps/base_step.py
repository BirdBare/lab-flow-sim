import typing
import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..swimlane import Swimlane

if typing.TYPE_CHECKING:
    from .function_step import FunctionStep
    from .process_step import ProcessStep


class BaseStep(models.Model):
    polymorphic_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    swimlane = models.ForeignKey(to=Swimlane, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.polymorphic_content_type = ContentType.objects.get_for_model(self.__class__)

        super().save(*args, **kwargs)

    def cast(self) -> FunctionStep | ProcessStep:
        model_class = self.polymorphic_content_type.model_class()

        if model_class is None:
            raise AttributeError("polymorphic_content_type is not set... This should never happen.")

        if model_class == BaseStep:
            raise TypeError("Step content type is BaseStep... This should never happen")

        return typing.cast("FunctionStep | ProcessStep", model_class.objects.get(pk=self.pk))
