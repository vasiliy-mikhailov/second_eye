import graphene_frame

class Person(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.String())
        name = graphene_frame.String()

    def __str__(self):
        return self.name
