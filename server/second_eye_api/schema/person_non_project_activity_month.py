import graphene_frame

from . import field_pack
from . import non_project_activity
from . import person
from . import person_non_project_activity_month

class PersonNonProjectActivityMonthTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person_month_id = graphene_frame.Int()
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        month = graphene_frame.Date()
        non_project_activity = graphene_frame.Field(to_entity=lambda: non_project_activity.NonProjectActivity)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPack(),
        ]