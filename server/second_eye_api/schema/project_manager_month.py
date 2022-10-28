import graphene_frame

from . import field_pack
from . import project_manager

class ProjectManagerMonth(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())

        project_manager = graphene_frame.Field(to_entity=lambda: project_manager.ProjectManager)

        month = graphene_frame.Date()

        analysis_time_spent_fte = graphene_frame.Float()
        development_time_spent_fte = graphene_frame.Float()
        testing_time_spent_fte = graphene_frame.Float()
        management_time_spent_fte = graphene_frame.Float()
        incident_fixing_time_spent_fte = graphene_frame.Float()
        non_project_activity_time_spent_fte = graphene_frame.Float()

        time_spent_fte = graphene_frame.Float()

        working_days_in_month_occured = graphene_frame.Int()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]