import graphene_frame

class StateCategory(graphene_frame.DataFrameObjectType):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    NOT_SET = -1

    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name = graphene_frame.String()

    def __str__(self):
        return self.name