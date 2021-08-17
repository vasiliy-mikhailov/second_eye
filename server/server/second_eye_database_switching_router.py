from second_eye_api.models import ALL_MODELS
from second_eye_api.database_switching_router import DatabaseSwitchingRouter

class SecondEyeDatabaseSwitchingRouter(DatabaseSwitchingRouter):
    models = ALL_MODELS
    db1 = 'db1'
    db2 = 'db2'