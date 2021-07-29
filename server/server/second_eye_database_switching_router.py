from second_eye_api.models import *
from second_eye_api.database_switching_router import DatabaseSwitchingRouter

class SecondEyeDatabaseSwitchingRouter(DatabaseSwitchingRouter):
    models = [
        DedicatedTeam,
        ProjectTeam,
        ChangeRequest,
        SystemChangeRequest,
        Task,
        FunctionComponent,
        FunctionComponentKind,
        Skill,
        System
    ]
    db1 = 'db1'
    db2 = 'db2'