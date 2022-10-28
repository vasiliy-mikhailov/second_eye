import graphene_frame

from . import company

class NonProjectActivity(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()

        time_spent = graphene_frame.Float()

        company = graphene_frame.Field(to_entity=lambda: company.Company)

    def __str__(self):
        return self.name