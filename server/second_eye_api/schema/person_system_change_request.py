import graphene_frame

from . import field_pack
from . import person
from . import system_change_request

class PersonSystemChangeRequestTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        system_change_request = graphene_frame.Field(to_entity=lambda: system_change_request.SystemChangeRequest)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
        ]