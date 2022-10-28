import pandas as pd

class SystemsCreator:
    def __init__(self):
        self.last_id = 14
        self.systems = [{
            "id": -1,
            "name": "Не указано",
        }]

    def create_system(self, name):
        id = self.last_id + 100
        systems = self.systems
        systems.append(
            {
                "id": id,
                "name": name,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        systems = self.systems
        self.data = pd.DataFrame(systems)