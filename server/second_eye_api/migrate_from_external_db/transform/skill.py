import cubista

class Skill(cubista.Table):
    ANALYSIS = 1
    DEVELOPMENT = 2
    TESTING = 3
    MANAGEMENT = 4
    INCIDENT_FIXING = 5
    NOT_SET = -1

    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()