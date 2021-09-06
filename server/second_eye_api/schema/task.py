import graphene_frame
from second_eye_api.schema import system
from second_eye_api.schema import state
from second_eye_api.schema import state_category
from second_eye_api.schema import dedicated_team
from second_eye_api.schema import project_team
from second_eye_api.schema import change_request
from second_eye_api.schema import planning_period
from second_eye_api.schema import skill
from second_eye_api.schema import system_change_request

class Task(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.String())
        url = graphene_frame.String()
        name = graphene_frame.String()

        preliminary_estimate = graphene_frame.Float(nulls=True)
        planned_estimate = graphene_frame.Float(nulls=True)
        time_spent = graphene_frame.Float(nulls=False)

        skill = graphene_frame.Field(to_entity=lambda: skill.Skill)
        state = graphene_frame.Field(to_entity=lambda: state.State)
        has_value = graphene_frame.Boolean()
        state_category = graphene_frame.Field(to_entity=lambda: state_category.StateCategory)
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        change_request = graphene_frame.Field(to_entity=lambda: change_request.ChangeRequest)
        system_change_request = graphene_frame.Field(to_entity=lambda: system_change_request.SystemChangeRequest)
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system = graphene_frame.Field(to_entity=lambda: system.System)

        estimate = graphene_frame.Float(nulls=False)
        time_left = graphene_frame.Float(nulls=False)

    def __str__(self):
        return self.name