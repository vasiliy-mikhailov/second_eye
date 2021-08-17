from .entities import EntitiesLoader

class Loader:
    def __init__(self, output_data, output_database):
        self.output_data = output_data
        self.output_database = output_database

    def load(self):
        output_data = self.output_data
        output_database = self.output_database

        entities_loader = EntitiesLoader(output_data=output_data, output_database=output_database)
        entities_loader.load()