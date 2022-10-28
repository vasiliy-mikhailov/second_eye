import graphene_frame

from . import field_pack
from . import non_project_activity
from . import person

class PersonNonProjectActivityTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        non_project_activity = graphene_frame.Field(to_entity=lambda: non_project_activity.NonProjectActivity)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
        ]