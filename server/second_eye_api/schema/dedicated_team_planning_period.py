import graphene_frame

from . import change_request
from . import dedicated_team
from . import dedicated_team_planning_period
from . import field_pack
from . import person
from . import planning_period
from . import project_team
from . import project_team_planning_period
from . import system
from . import system_change_request

class DedicatedTeamPlanningPeriod(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        project_teams = graphene_frame.ManyToMany(
            to_entity=lambda: project_team.ProjectTeam,
            to_field="project_team_id",
            through_entity=lambda: project_team.ProjectTeamPlanningPeriod,
            through_field="dedicated_team_planning_period_id"
        )

        project_team_planning_periods = graphene_frame.List(to_entity=lambda: project_team_planning_period.ProjectTeamPlanningPeriod, to_field="dedicated_team_planning_period_id")

        change_requests = graphene_frame.List(to_entity=lambda: change_request.ChangeRequest, to_field="dedicated_team_planning_period_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: DedicatedTeamPlanningPeriodTimeSheetsByDate, to_field="dedicated_team_planning_period_id")

        dedicated_team_planning_period_systems = graphene_frame.List(
            to_entity=lambda: DedicatedTeamPlanningPeriodSystem,
            to_field="dedicated_team_planning_period_id"
        )

        estimate = graphene_frame.Float()
        time_left = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        positionPersons = graphene_frame.List(to_entity=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriodPositionPersonTimeSpent, to_field="dedicated_team_planning_period_id")

        time_spent_for_reengineering_percent = graphene_frame.Float()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class DedicatedTeamPlanningPeriodTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        time_spent_with_value_percent_cumsum = graphene_frame.Float()
        time_spent_without_value_percent_cumsum = graphene_frame.Float()

        time_spent_for_reengineering_percent_cumsum = graphene_frame.Float()
        time_spent_not_for_reengineering_percent_cumsum = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: DedicatedTeamPlanningPeriod)

class DedicatedTeamPlanningPeriodPositionPersonTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        position = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeamPosition)
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        dedicated_team_planning_period = graphene_frame.Field(to_entity=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod)
        total_capacity_fte = graphene_frame.Float()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class DedicatedTeamPlanningPeriodSystem(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system = graphene_frame.Field(to_entity=lambda: system.System)
        project_team_planning_period_systems = graphene_frame.List(to_entity=lambda: project_team_planning_period.ProjectTeamPlanningPeriodSystem, to_field="dedicated_team_planning_period_system_id")

        system_change_requests = graphene_frame.List(to_entity=lambda: system_change_request.SystemChangeRequest, to_field="dedicated_team_planning_period_system_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: DedicatedTeamPlanningPeriodSystemTimeSheetsByDate, to_field="dedicated_team_planning_period_system_id")

        estimate = graphene_frame.Float()
        time_spent = graphene_frame.Float()
        time_left = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

class DedicatedTeamPlanningPeriodSystemTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: DedicatedTeamPlanningPeriod)