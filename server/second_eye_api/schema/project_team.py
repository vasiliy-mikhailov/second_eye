import graphene_frame
from second_eye_api.schema import dedicated_team
from second_eye_api.schema import planning_period
from second_eye_api.schema import change_request

class ProjectTeam(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name = graphene_frame.String()

        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)

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

class ProjectTeamPlanningPeriod(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        project_team = graphene_frame.Field(to_entity=lambda: ProjectTeam)
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)

        change_requests = graphene_frame.List(to_entity=lambda: change_request.ChangeRequest, to_field="project_team_planning_period_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: ProjectTeamPlanningPeriodTimeSheetsByDate, to_field="project_team_planning_period_id")

        time_spent_percent_with_value_and_without_value_by_date = graphene_frame.List(
            to_entity=lambda: ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate,
            to_field = "project_team_planning_period_id"
        )

        estimate = graphene_frame.Float()
        time_spent = graphene_frame.Float()
        time_left = graphene_frame.Float()


class ProjectTeamPlanningPeriodTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: ProjectTeamPlanningPeriod)

class ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent_with_value_percent_cumsum = graphene_frame.Float()
        time_spent_without_value_percent_cumsum = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: ProjectTeamPlanningPeriod)