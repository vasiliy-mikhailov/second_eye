def test_companies_loaded(graphene_client):
    executed = graphene_client.execute(
"""
{ 
    companies {
        id
        name
    } 
}
"""
)
    assert executed == {
        "data": {
            "companies": [
                { "id": 1, "name": "Банк" },
                { "id": 2, "name": "Брокер" },
                { "id": 3, "name": "Телеком" },
            ]
        }
    }


def test_dedicated_teams_loaded(graphene_client):
    executed = graphene_client.execute(
"""
{ 
    dedicatedTeams {
        id
        name
        company {
            id
        }
    } 
}
"""
)
    assert executed == {
        "data": {
            "dedicatedTeams": [
                { "id": -1, "name": "Не указано", "company": { "id": 1} },
                { "id": 1, "name": "Корпоративный блок", "company": {"id": 1}},
                { "id": 2, "name": "Розничный блок", "company": {"id": 1}},
                { "id": 3, "name": "Инвестиционный блок", "company": {"id": 1}},
                { "id": 4, "name": "Прайват банкинг", "company": {"id": 1}},
                { "id": 5, "name": "Бекофис", "company": {"id": 1}},
            ]
        }
    }

def test_project_teams_loaded(graphene_client):
    executed = graphene_client.execute(
"""
{ 
    projectTeams {
        id
        name
        dedicatedTeam {
            id
        }
    } 
}
"""
)
    assert executed == {
        "data": {
            "projectTeams": [
                { "id": -1, "name": "Не указано", "dedicatedTeam": { "id": -1} },
                { "id": 1, "name": "Крупный бизнес", "dedicatedTeam": {"id": 1} },
                { "id": 2, "name": "Средний бизнес", "dedicatedTeam": {"id": 1} },
                { "id": 3, "name": "Малый и микробизнес", "dedicatedTeam": {"id": 1} },
                { "id": 4, "name": "Привлечение, онбординг и процессы обслуживания корпоратов", "dedicatedTeam": {"id": 1} },
                { "id": 5, "name": "Дистанционное банковское обслуживание", "dedicatedTeam": {"id": 1} },
                { "id": 6, "name": "Факторинг", "dedicatedTeam": {"id": 1} },
                { "id": 7, "name": "Корпоративное кредитование", "dedicatedTeam": {"id": 1} },
                { "id": 8, "name": "Корпоративные депозиты", "dedicatedTeam": {"id": 1} },
            ]
        }
    }

def test_project_teams_loaded(graphene_client):
    executed = graphene_client.execute(
"""
{ 
    planningPeriods {
        id
        name
    } 
}
"""
)
    assert executed == {
        "data": {
            "planningPeriods": [
                { "id": -1, "name": "Не указано" },
                { "id": 2021, "name": "2021" },
                { "id": 2022, "name": "2022" },
            ]
        }
    }

def test_systems_loaded(graphene_client):
    executed = graphene_client.execute(
"""
{ 
    systems {
        id
        name
    } 
}
"""
)
    assert executed == {
        "data": {
            "systems": [
                {"id": -1, "name": "Не указано"},
                {"id": 1, "name": "Интернет-фронт ДБО ЮЛ"},
                {"id": 2, "name": "iOS-фронт ДБО ЮЛ"},
                {"id": 3, "name": "Android-фронт ДБО ЮЛ"},
                {"id": 4, "name": "Бек ДБО ЮЛ"},
                {"id": 5, "name": "Шина"},
                {"id": 6, "name": "АБС ЦФТ"},
                {"id": 7, "name": "Siebel CRM"},
                {"id": 8, "name": "Camunda BPM"},
                {"id": 9, "name": "Электронный архив документов"},
            ]
        }
    }