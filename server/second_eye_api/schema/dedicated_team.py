import graphene_frame

from . import company
from . import dedicated_team
from . import dedicated_team_planning_period
from . import field_pack
from . import person
from . import project_team
from . import skill
from . import system

class DedicatedTeam(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name = graphene_frame.String()

        company = graphene_frame.Field(to_entity=lambda: company.Company)

        cio = graphene_frame.Field(to_entity=lambda: person.Person)
        cto = graphene_frame.Field(to_entity=lambda: person.Person)

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: dedicated_team.DedicatedTeamTimeSheetsByDate, to_field="dedicated_team_id")

        actual_change_request_capacity = graphene_frame.Float()
        estimate = graphene_frame.Float()
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
        positions = graphene_frame.List(to_entity=lambda: dedicated_team.DedicatedTeamPosition, to_field="dedicated_team_id")

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        dedicated_team_planning_periods = graphene_frame.List(
            to_entity=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod,
            to_field="dedicated_team_id"
        )

        time_spent_for_reengineering_percent = graphene_frame.Float()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class DedicatedTeamTimeSheetsByDate(graphene_frame.DataFrameObjectType):
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

        dedicated_team = graphene_frame.Field(to_entity=lambda: DedicatedTeam)


class DedicatedTeamPosition(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        url = graphene_frame.String()
        name = graphene_frame.String()
        change_request_capacity = graphene_frame.Float()

        dedicated_team = graphene_frame.Field(to_entity=lambda: DedicatedTeam)

        person = graphene_frame.Field(to_entity=lambda: person.Person)

        abilities = graphene_frame.List(to_entity=lambda: dedicated_team.DedicatedTeamPositionAbility, to_field="dedicated_team_position_id")

    def __str__(self):
        return self.name

class DedicatedTeamPositionAbility(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        dedicated_team_position = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeamPosition)

        skill = graphene_frame.Field(to_entity=lambda: skill.Skill)

        system = graphene_frame.Field(to_entity=lambda: system.System)

    def __str__(self):
        return '{} {}'.format(self.skill, self.system)




