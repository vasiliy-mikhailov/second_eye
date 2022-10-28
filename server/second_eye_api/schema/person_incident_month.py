import graphene_frame

from . import field_pack
from . import incident
from . import person

class PersonIncidentMonthTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person_month_id = graphene_frame.Int()
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        month = graphene_frame.Date()
        incident = graphene_frame.Field(to_entity=lambda: incident.Incident)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPack(),
        ]