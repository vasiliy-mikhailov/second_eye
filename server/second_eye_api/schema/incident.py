import graphene_frame

from . import project_team

class Incident(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()

        time_spent = graphene_frame.Float()

        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)

    def __str__(self):
        return self.name