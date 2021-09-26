import pandas as pd

class SystemsExtractor:
    def extract(self):
        system_not_specified = pd.DataFrame([
                [-1, "Не указано"],
                [1, "Интернет-фронт ДБО ЮЛ"],
                [2, "iOS-фронт ДБО ЮЛ"],
                [3, "Android-фронт ДБО ЮЛ"],
                [4, "Бек ДБО ЮЛ"],
                [5, "Шина"],
                [6, "АБС ЦФТ"],
                [7, "Siebel CRM"],
                [8, "Camunda BPM"],
                [9, "Электронный архив документов"],
            ], columns=["id", "name"]
        )

        self.data = system_not_specified