import pandas as pd

class EpicsCreator:
    def __init__(self):
        self.last_id = 4
        self.epics = [{
            "id": -1,
            "key": "-1",
            "name": "Не указано",
            "url": "",
            "company_id": -1,
        }]

    def create_epic(self, key, name, url="", company_id=-1):
        id = self.last_id + 100
        epics = self.epics
        epics.append(
            {
                "id": id,
                "key": key,
                "name": name,
                "url": url,
                "company_id": company_id,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        epics = self.epics
        self.data = pd.DataFrame(epics)