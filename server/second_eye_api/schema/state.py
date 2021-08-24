import graphene_frame
from .state_category import StateCategory

class State(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name =graphene_frame.String()

        category = graphene_frame.Field(to_entity=lambda: StateCategory)

    def __str__(self):
        return self.name
