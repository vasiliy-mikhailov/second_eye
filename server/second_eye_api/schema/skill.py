import graphene_frame

class Skill(graphene_frame.DataFrameObjectType):
    ANALYSIS = 1
    DEVELOPMENT = 2
    TESTING = 3
    NOT_SET = -1

    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name = graphene_frame.String()

    def __str__(self):
        return self.name