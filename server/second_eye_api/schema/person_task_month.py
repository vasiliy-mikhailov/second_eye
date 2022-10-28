import graphene_frame

from . import field_pack
from . import person
from . import person_task_month
from . import task

class PersonTaskMonthTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person_month_id = graphene_frame.Int()
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        month = graphene_frame.Date()
        task = graphene_frame.Field(to_entity=lambda: task.Task)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPack(),
        ]