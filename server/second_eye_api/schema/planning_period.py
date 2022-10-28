import graphene_frame
from . import change_request
from . import dedicated_team
from . import dedicated_team_planning_period
from . import field_pack
from . import person
from . import project_team
from . import project_team_planning_period
from . import quarter
from . import system

class PlanningPeriod(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name = graphene_frame.String()
        start = graphene_frame.Date()
        end = graphene_frame.Date()

        project_teams = graphene_frame.ManyToMany(
            to_entity=lambda: project_team.ProjectTeam,
            to_field="project_team_id",
            through_entity=lambda: project_team.ProjectTeamPlanningPeriod,
            through_field="planning_period_id"
        )

        dedicated_teams = graphene_frame.ManyToMany(
            to_entity=lambda: dedicated_team.DedicatedTeam,
            to_field="dedicated_team_id",
            through_entity=lambda: dedicated_team.DedicatedTeamPlanningPeriod,
            through_field="planning_period_id"
        )

        dedicated_team_planning_periods = graphene_frame.List(to_entity=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod, to_field="planning_period_id")
        project_team_planning_periods = graphene_frame.List(to_entity=lambda: project_team_planning_period.ProjectTeamPlanningPeriod, to_field="planning_period_id")

        systems = graphene_frame.ManyToMany(
            to_entity=lambda: system.System,
            to_field="system_id",
            through_entity=lambda: system.SystemPlanningPeriod,
            through_field="planning_period_id"
        )

        system_planning_periods = graphene_frame.List(to_entity=lambda: system.SystemPlanningPeriod, to_field="planning_period_id")

        estimate = graphene_frame.Float()
        time_left = graphene_frame.Float()

        change_requests = graphene_frame.List(to_entity=lambda: change_request.ChangeRequest, to_field="planning_period_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: PlanningPeriodTimeSheetsByDate, to_field="planning_period_id")

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        time_sheets_by_date_model_m = graphene_frame.Float()
        time_sheets_by_date_model_b = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        persons = graphene_frame.List(to_entity=lambda: person.PersonPlanningPeriodTimeSpent, to_field="planning_period_id")

        quarters = graphene_frame.List(to_entity=lambda: quarter.Quarter, to_field="planning_period_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class PlanningPeriodTimeSheetsByDate(graphene_frame.DataFrameObjectType):
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

        planning_period = graphene_frame.Field(to_entity=lambda: PlanningPeriod)

