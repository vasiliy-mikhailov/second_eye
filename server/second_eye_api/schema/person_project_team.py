import graphene_frame

from . import field_pack
from . import person
from . import person_project_team
from . import project_team

class PersonProjectTeamTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
        ]
