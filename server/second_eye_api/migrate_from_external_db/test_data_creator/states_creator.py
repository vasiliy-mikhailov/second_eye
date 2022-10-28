import pandas as pd

class StatesCreator:
    DONE_ID = "3"

    def extract(self):
        states = [
            ("-1", 'Не указано'),
            (StatesCreator.DONE_ID, "Выполнена"),
        ]

        self.data = pd.DataFrame.from_records(states, columns=["id", "name"])
