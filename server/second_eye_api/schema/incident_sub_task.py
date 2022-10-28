import graphene_frame
from . import dedicated_team
from . import incident
from . import person
from . import planning_period
from . import project_team
from . import skill
from . import system
from . import state
from . import state_category
from . import system_change_request

class IncidentSubTask(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()

        time_spent = graphene_frame.Float(nulls=False)
        time_original_estimate = graphene_frame.Float(nulls=False)

        skill = graphene_frame.Field(to_entity=lambda: skill.Skill)
        state = graphene_frame.Field(to_entity=lambda: state.State)

        state_category = graphene_frame.Field(to_entity=lambda: state_category.StateCategory)
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        incident = graphene_frame.Field(to_entity=lambda: incident.Incident)
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)

        estimate = graphene_frame.Float(nulls=False)
        time_left = graphene_frame.Float(nulls=False)

    def __str__(self):
        return self.name