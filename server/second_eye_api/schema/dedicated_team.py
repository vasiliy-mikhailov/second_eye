import graphene_frame
from second_eye_api.schema import company
from second_eye_api.schema import project_team
from second_eye_api.schema import planning_period
from second_eye_api.schema import change_request

class DedicatedTeam(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name = graphene_frame.String()

        company = graphene_frame.Field(to_entity=lambda: company.Company)

        actual_change_request_capacity = graphene_frame.Float()
        time_left = graphene_frame.Float()
        queue_length = graphene_frame.Float()

        actual_analysis_capacity = graphene_frame.Float()
        analysis_time_left = graphene_frame.Float()
        analysis_queue_length = graphene_frame.Float()

        actual_development_capacity = graphene_frame.Float()
        development_time_left = graphene_frame.Float()
        development_queue_length = graphene_frame.Float()

        actual_testing_capacity = graphene_frame.Float()
        testing_time_left = graphene_frame.Float()
        testing_queue_length = graphene_frame.Float()

    def __str__(self):
        return self.name

class DedicatedTeamPlanningPeriod(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        dedicated_team = graphene_frame.Field(to_entity=lambda: DedicatedTeam)
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        project_teams = graphene_frame.ManyToMany(
            to_entity=lambda: project_team.ProjectTeam,
            to_field="project_team_id",
            through_entity=lambda: project_team.ProjectTeamPlanningPeriod,
            through_field="dedicated_team_planning_period_id"
        )

        change_requests = graphene_frame.List(to_entity=lambda: change_request.ChangeRequest, to_field="dedicated_team_planning_period_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: DedicatedTeamPlanningPeriodTimeSheetsByDate, to_field="dedicated_team_planning_period_id")

        time_spent_percent_with_value_and_without_value_by_date = graphene_frame.List(
            to_entity=lambda: DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate,
            to_field = "dedicated_team_planning_period_id"
        )

        estimate = graphene_frame.Float()
        time_spent = graphene_frame.Float()
        time_left = graphene_frame.Float()

class DedicatedTeamPlanningPeriodTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: DedicatedTeamPlanningPeriod)

class DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent_with_value_percent_cumsum = graphene_frame.Float()
        time_spent_without_value_percent_cumsum = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: DedicatedTeamPlanningPeriod)