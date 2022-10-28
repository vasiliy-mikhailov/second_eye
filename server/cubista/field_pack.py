import copy

class FieldPack:
    class Fields:
        pass

    def apply_to_table(self, table):
        fields = { key: value for key, value in self.Fields.__dict__.items() if not key.startswith("__") }

        table_fields = table.Fields

        for field_name, field_object in fields.items():
            field_object_copy = copy.copy(field_object)
            setattr(table_fields, field_name, field_object_copy)