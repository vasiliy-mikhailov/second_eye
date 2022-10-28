import graphene_frame

from . import field_pack
from . import person
from . import task

class PersonTaskTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        task = graphene_frame.Field(to_entity=lambda: task.Task)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
        ]