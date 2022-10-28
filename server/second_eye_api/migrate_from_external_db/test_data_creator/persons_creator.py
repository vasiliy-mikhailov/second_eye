import pandas as pd

class PersonsCreator:
    def __init__(self):
        self.last_id = 11
        self.persons = [{
            "id": -1,
            "key": "-1",
            "name": "Не указано",
            "is_active": 0,
        }]

    def create_person(self, name="", is_active=1):
        id = self.last_id + 100
        key = str(id)
        persons = self.persons
        persons.append(
            {
                "id": id,
                "key": key,
                "name": name,
                "is_active": is_active,
            }
        )

        self.last_id = id
        return id, key

    def extract(self):
        persons = self.persons
        self.data = pd.DataFrame(persons)