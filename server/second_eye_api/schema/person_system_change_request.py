import graphene_frame

from . import field_pack
from . import person
from . import system_change_request

class PersonSystemChangeRequestTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        person_key = graphene_frame.String()
        system_change_request = graphene_frame.Field(to_entity=lambda: system_change_request.SystemChangeRequest)
        system_change_request_key = graphene_frame.String()
        system_change_request_effort_per_function_point = graphene_frame.Float()

        function_points_effort = graphene_frame.Float()
        person_planning_period_function_points_effort = graphene_frame.Float()
        percentage_of_person_total_time_in_planning_period = graphene_frame.Float()
        effort_per_function_point_weighted_by_person_total_time_in_planning_period = graphene_frame.Float()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
        ]