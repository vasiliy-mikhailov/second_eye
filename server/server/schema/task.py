from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"


class TaskTimeSheetsType(DjangoObjectType):
    class Meta:
        model = TaskTimeSheets
        fields = "__all__"


class TaskTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = TaskTimeSheetsByDate
        fields = "__all__"