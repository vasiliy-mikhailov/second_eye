from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class SkillType(DjangoObjectType):
    class Meta:
        model = Skill
        fields = "__all__"