import graphene_frame

from . import field_pack
from . import person
from . import project_team

class PersonProjectTeamMonth(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        person_id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person_key = graphene_frame.String()
        person_name = graphene_frame.String()
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        month = graphene_frame.Date()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]