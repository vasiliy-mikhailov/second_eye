import graphene_frame

from . import field_pack
from . import project_manager_month
from . import project_team

class ProjectManager(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        name = graphene_frame.String()
        is_active = graphene_frame.Int()

        months = graphene_frame.List(to_entity=lambda: project_manager_month.ProjectManagerMonth, to_field="project_manager_id")
        project_teams = graphene_frame.List(to_entity=lambda: project_team.ProjectTeam, to_field="project_manager_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]