import graphene_frame
from second_eye_api.schema import company
from second_eye_api.schema import project_team
from second_eye_api.schema import planning_period
from second_eye_api.schema import change_request
from second_eye_api.schema import person
from second_eye_api.schema import skill
from second_eye_api.schema import system

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

        project_teams = graphene_frame.List(to_entity=lambda : project_team.ProjectTeam, to_field="dedicated_team_id")
        positions = graphene_frame.List(to_entity=lambda: DedicatedTeamPosition, to_field="dedicated_team_id")

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

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

        project_team_planning_periods = graphene_frame.List(to_entity=lambda: project_team.ProjectTeamPlanningPeriod, to_field="dedicated_team_planning_period_id")

        change_requests = graphene_frame.List(to_entity=lambda: change_request.ChangeRequest, to_field="dedicated_team_planning_period_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: DedicatedTeamPlanningPeriodTimeSheetsByDate, to_field="dedicated_team_planning_period_id")

        time_spent_cumsum_at_end_prediction = graphene_frame.Float()

        time_spent_percent_with_value_and_without_value_by_date = graphene_frame.List(
            to_entity=lambda: DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate,
            to_field = "dedicated_team_planning_period_id"
        )

        estimate = graphene_frame.Float()
        time_spent = graphene_frame.Float()
        time_left = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

class DedicatedTeamPlanningPeriodTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: DedicatedTeamPlanningPeriod)

class DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent_with_value_percent_cumsum = graphene_frame.Float()
        time_spent_without_value_percent_cumsum = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: DedicatedTeamPlanningPeriod)


class DedicatedTeamPosition(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        url = graphene_frame.String()
        name = graphene_frame.String()
        change_request_capacity = graphene_frame.Float()

        dedicated_team = graphene_frame.Field(to_entity=lambda: DedicatedTeam)

        person = graphene_frame.Field(to_entity=lambda: person.Person)

        abilities = graphene_frame.List(to_entity=lambda: DedicatedTeamPositionAbility, to_field="dedicated_team_position_id")

    def __str__(self):
        return self.name

class DedicatedTeamPositionAbility(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        dedicated_team_position = graphene_frame.Field(to_entity=lambda: DedicatedTeamPosition)

        skill = graphene_frame.Field(to_entity=lambda: skill.Skill)

        system = graphene_frame.Field(to_entity=lambda: system.System)

    def __str__(self):
        return '{} {}'.format(self.skill, self.system)

