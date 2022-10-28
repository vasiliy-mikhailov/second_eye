import graphene_frame
from . import change_request
from . import dedicated_team
from . import person
from . import planning_period
from . import project_team
from . import skill
from . import system
from . import state
from . import state_category
from . import system_change_request

class Task(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()

        preliminary_estimate = graphene_frame.Float(nulls=True)
        planned_estimate = graphene_frame.Float(nulls=True)
        time_spent = graphene_frame.Float(nulls=False)
        time_original_estimate = graphene_frame.Float(nulls=False)

        skill = graphene_frame.Field(to_entity=lambda: skill.Skill)
        state = graphene_frame.Field(to_entity=lambda: state.State)
        has_value = graphene_frame.Boolean()
        is_reengineering = graphene_frame.Boolean()
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