import graphene_frame

from . import field_pack
from . import person
from . import person_incident_month
from . import person_non_project_activity_month
from . import person_system_change_request_month
from . import person_task_month

class PersonMonthTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        person_id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person_key = graphene_frame.String()
        month = graphene_frame.Date()
        incidents = graphene_frame.List(to_entity=lambda: person_incident_month.PersonIncidentMonthTimeSpent, to_field="person_month_id")
        non_project_activities = graphene_frame.List(to_entity=lambda: person_non_project_activity_month.PersonNonProjectActivityMonthTimeSpent, to_field="person_month_id")
        system_change_requests = graphene_frame.List(to_entity=lambda: person_system_change_request_month.PersonSystemChangeRequestMonthTimeSpent, to_field="person_month_id")
        tasks = graphene_frame.List(to_entity=lambda: person_task_month.PersonTaskMonthTimeSpent, to_field="person_month_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]