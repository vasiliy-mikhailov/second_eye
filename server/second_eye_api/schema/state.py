import graphene_frame
from . import change_request
from . import system_change_request
from . import state_category
from . import task

class State(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.String())
        name =graphene_frame.String()

        category = graphene_frame.Field(to_entity=lambda: state_category.StateCategory)

        change_requests = graphene_frame.List(to_entity=lambda: change_request.ChangeRequest, to_field="state_id")

        system_change_requests = graphene_frame.List(to_entity=lambda: system_change_request.SystemChangeRequest, to_field="state_id")

        tasks = graphene_frame.List(to_entity=lambda: task.Task, to_field="state_id")

    def __str__(self):
        return self.name
