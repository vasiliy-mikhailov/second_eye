import graphene_frame

from . import field_pack
from . import person
from . import system_change_request

class PersonSystemChangeRequestMonthTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person_month_id = graphene_frame.Int()
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        month = graphene_frame.Date()
        system_change_request = graphene_frame.Field(to_entity=lambda: system_change_request.SystemChangeRequest)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPack(),
        ]