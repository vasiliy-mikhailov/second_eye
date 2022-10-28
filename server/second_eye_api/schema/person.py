import graphene_frame

from . import epic
from . import field_pack
from . import person
from . import person_change_request
from . import person_dedicated_team
from . import person_incident
from . import person_non_project_activity
from . import person_project_team
from . import person_system
from . import person_system_change_request
from . import person_task
from . import planning_period
from . import project_team
from . import system
from . import system_change_request
from . import task

class Person(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        name = graphene_frame.String()
        planning_periods = graphene_frame.List(to_entity=lambda: PersonPlanningPeriodTimeSpent, to_field="person_id")
        main_project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        is_outsource = graphene_frame.Boolean()
        is_active = graphene_frame.Boolean()
        change_requests = graphene_frame.List(to_entity=lambda: person_change_request.PersonChangeRequestTimeSpent, to_field="person_id")
        dedicated_teams = graphene_frame.List(to_entity=lambda: person_dedicated_team.PersonDedicatedTeamTimeSpent, to_field="person_id")
        incidents = graphene_frame.List(to_entity=lambda: person_incident.PersonIncidentTimeSpent, to_field="person_id")
        non_project_activities = graphene_frame.List(to_entity=lambda: person_non_project_activity.PersonNonProjectActivityTimeSpent, to_field="person_id")
        project_team_position_persons = graphene_frame.List(to_entity=lambda: project_team.ProjectTeamPositionPersonTimeSpent, to_field="person_id")
        project_teams = graphene_frame.List(to_entity=lambda: person_project_team.PersonProjectTeamTimeSpent, to_field="person_id")
        systems = graphene_frame.List(to_entity=lambda: person_system.PersonSystemTimeSpent, to_field="person_id")
        system_change_requests = graphene_frame.List(to_entity=lambda: person_system_change_request.PersonSystemChangeRequestTimeSpent, to_field="person_id")
        tasks = graphene_frame.List(to_entity=lambda: person_task.PersonTaskTimeSpent, to_field="person_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
        ]

    def __str__(self):
        return self.name

class PersonEpicTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: Person)
        epic = graphene_frame.Field(to_entity=lambda: epic.Epic)

class PersonPlanningPeriodTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: Person)
        person_id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person_key = graphene_frame.String()
        person_name = graphene_frame.String()
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system_change_requests = graphene_frame.List(to_entity=lambda: person_system_change_request.PersonSystemChangeRequestTimeSpent, to_field="person_planning_period_id")
        effort_per_function_point = graphene_frame.Float()

class PersonProjectTeamPlanningPeriodTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: Person)
        project_team_planning_period = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeamPlanningPeriod)

class PersonSystemChangeRequestTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=Person)
        person_key = graphene_frame.String()
        system_change_request = graphene_frame.Field(to_entity=lambda: system_change_request.SystemChangeRequest)
        system_change_request_key = graphene_frame.String()
        date = graphene_frame.Date()
        time_spent = graphene_frame.Float()



