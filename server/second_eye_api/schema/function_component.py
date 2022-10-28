import graphene_frame
from . import state
from . import system_change_request

class FunctionComponent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()

        system_change_request = graphene_frame.Field(to_entity=lambda: system_change_request.SystemChangeRequest)

        state = graphene_frame.Field(to_entity=lambda: state.State)

        count = graphene_frame.Int()

        function_points = graphene_frame.Float()

    def __str__(self):
        return self.name