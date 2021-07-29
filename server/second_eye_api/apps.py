from django.apps import AppConfig
from django.core.management import call_command

class SecondEyeApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'second_eye_api'

    def migrate(self, db):
        try:
            call_command(
                'migrate',
                app_label='second_eye_api',
                verbosity=1,
                interactive=False,
                database=db
            )
        except:
            pass

    def ready(self):
        self.migrate(db='default')
        self.migrate(db='db1')
        self.migrate(db='db2')
