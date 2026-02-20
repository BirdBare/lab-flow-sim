from django.contrib import admin

from .models import FunctionStep, Process, ProcessStep, StepIndex, Swimlane, SwimlaneIndex

admin.site.register(Process)
admin.site.register(Swimlane)
admin.site.register(SwimlaneIndex)
admin.site.register(ProcessStep)
admin.site.register(FunctionStep)
admin.site.register(StepIndex)
