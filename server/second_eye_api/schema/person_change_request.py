import graphene_frame

from . import change_request
from . import field_pack
from . import person

class PersonChangeRequestTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        change_request = graphene_frame.Field(to_entity=lambda: change_request.ChangeRequest)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
        ]