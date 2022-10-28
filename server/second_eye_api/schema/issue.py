import graphene_frame
from . import change_request
from . import dedicated_team
from . import epic
from . import person
from . import planning_period
from . import project_team
from . import project_team_quarter
from . import quarter
from . import system_change_request
from . import task

class ProjectTeamPositionPersonPlanFactIssue(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        position = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeamPosition)
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        new_functions_plan_fact_fte_difference = graphene_frame.Float(nulls=False)

class ChangeRequestCalculatedDateAfterQuarterEndIssue(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        change_request = graphene_frame.Field(to_entity=lambda: change_request.ChangeRequest)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        quarter = graphene_frame.Field(to_entity=lambda: quarter.Quarter)
        project_team_quarter = graphene_frame.Field(to_entity=lambda: project_team_quarter.ProjectTeamQuarter)
        quarter_end_delay_days = graphene_frame.Int(nulls=False)