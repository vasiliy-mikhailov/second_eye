class DatabaseSwitchingRouter:
    models = []
    db1 = None
    db2 = None

    def __init__(self):
        self.database_for_write = self.db1
        self.database_for_read = self.db2

    def db_for_read(self, model, **hints):
        """
        Return one of the replicas
        """

        if model in self.models:
            return self.database_for_read
        else:
            return None

    def db_for_write(self, model, **hints):
        # Always return the default database

        if model in self.models:
            return self.database_for_write
        else:
            return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

    def switch_databases(self):
        self.database_for_write, self.database_for_read = self.database_for_read, self.database_for_write