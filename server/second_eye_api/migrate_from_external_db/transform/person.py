import cubista

class Person(cubista.Table):
    class Fields:
        id = cubista.StringField(primary_key=True, unique=True)
        name = cubista.StringField()
        is_active = cubista.IntField()