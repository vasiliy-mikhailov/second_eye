from second_eye_api.models import *
import django.db
import pandas as pd
import numpy as np

def get_model_field_names(model):
    return [
        field.attname if hasattr(field, 'attname') else field.name
        for field in model._meta.concrete_fields
    ]

def save_dataframe_to_db(dataframe, model):
    model_field_names = get_model_field_names(model)

    reduced_dataframe = dataframe.reset_index()[model_field_names]

    model.objects.bulk_create(
        Skill(**vals) for vals in reduced_dataframe.to_dict('records')
    )

def fill_skills():
    skillsArray = np.array([
        (1, 'Аналитика'),
        (2, 'Разработка'),
        (3, 'Тестирование')
    ])

    df = pd.DataFrame.from_records(skillsArray, columns=['id', 'name'], index='id')

    save_dataframe_to_db(dataframe=df, model=Skill)

def find_database_switching_router():
    switch_databases_method_name = 'switch_databases'

    routers = django.db.router.routers

    for router in routers:
        try:
            _ = getattr(router, switch_databases_method_name)

            return router
        except AttributeError:
            # If the router doesn't have a method, skip to the next one.
            pass

    return None

def refill_internal_db():
    router = find_database_switching_router()
    db_to_refill = router.database_for_write

    System.objects.all().using(db_to_refill).delete()
    FunctionComponentKind.objects.all().using(db_to_refill).delete()
    DedicatedTeam.objects.all().using(db_to_refill).delete()
    ProjectTeam.objects.all().using(db_to_refill).delete()
    ChangeRequest.objects.all().using(db_to_refill).delete()
    SystemChangeRequest.objects.all().using(db_to_refill).delete()
    Task.objects.all().using(db_to_refill).delete()
    FunctionComponent.objects.all().using(db_to_refill).delete()
    Skill.objects.all().using(db_to_refill).delete()
    fill_skills()

    system_1 = System(id=1, name='System 1')
    system_1.save()

    function_component_kind_1 = FunctionComponentKind(id=1, name='Function component kind 1', weight=4)
    function_component_kind_1.save()

    dedicated_team_1 = DedicatedTeam(
        id=1,
        name='Dedicated team 1',
        url='https://url.com'
    )
    dedicated_team_1.save()

    project_team_1_1 = ProjectTeam(
        id=1,
        name='Project team 1.1',
        url='https://url.com',
        dedicated_team=dedicated_team_1
    )
    project_team_1_1.save()

    change_request_1_1_1 = ChangeRequest(
        id=1,
        name='Change request 1.1.1',
        url='https://url.com',
        project_team=project_team_1_1
    )
    change_request_1_1_1.save()

    system_change_request_1_1_1_1 = SystemChangeRequest(
        id=1,
        name='System change request 1.1.1.1',
        url='https://url.com',
        system=system_1,
        change_request=change_request_1_1_1
    )
    system_change_request_1_1_1_1.save()

    for i in range(1, 10):
        task_1_1_1_1_1 = Task(
            id=i,
            name='Task 1.1.1.1.1',
            url='https://url.com',
            skill_id=1,
            system_change_request=system_change_request_1_1_1_1
        )
        task_1_1_1_1_1.save()

        function_component_1_1_1_1_1_1 = FunctionComponent(
            id=1,
            name='Function component 1.1.1.1.1.1',
            url='https://url.com',
            function_component_kind=function_component_kind_1,
            task=task_1_1_1_1_1
        )
        function_component_1_1_1_1_1_1.save()

    dt2 = DedicatedTeam(id=2, name='Dedicated team 2', url='https://url.com')
    dt2.save()

    router.switch_databases()
