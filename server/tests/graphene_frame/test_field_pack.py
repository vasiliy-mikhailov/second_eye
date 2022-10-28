import pytest
import graphene_frame

def test_field_pack_adds_field():
    class FieldPack(graphene_frame.FieldPack):
        class Fields:
            field_from_field_pack = graphene_frame.String()

    class Frame(graphene_frame.DataFrameObjectType):
        class Fields:
            id = graphene_frame.Int()

        class FieldPacks:
            field_packs = [
                lambda: FieldPack(),
            ]

    frame = Frame()

    fields = frame.Fields

    assert "field_from_field_pack" in fields.__dict__

    field_from_field_pack = fields.__dict__["field_from_field_pack"]
    assert type(field_from_field_pack) is graphene_frame.String
