from second_eye_api.migrate_from_external_db.input_data import InputData
from second_eye_api.migrate_from_external_db.extract.skills_extractor import SkillsExtractor
from second_eye_api.migrate_from_external_db.extract.systems_extractor import SystemsExtractor
from second_eye_api.migrate_from_external_db.extract.dedicated_teams_extractor import DedicatedTeamsExtractor
from second_eye_api.migrate_from_external_db.extract.project_teams_extractor import ProjectTeamsExtractor
from second_eye_api.migrate_from_external_db.extract.change_requests_extractor import ChangeRequestsExtractor
from second_eye_api.migrate_from_external_db.extract.system_change_requests_extractor import SystemChangeRequestsExtractor
from second_eye_api.migrate_from_external_db.extract.tasks_extractor import TasksExtractor
from second_eye_api.migrate_from_external_db.extract.persons_extractor import PersonsExtractor
from second_eye_api.migrate_from_external_db.extract.dedicated_team_positions_extractor import DedicatedTeamPositionsExtractor
from second_eye_api.migrate_from_external_db.extract.project_team_positions_extractor import ProjectTeamPositionsExtractor
from second_eye_api.migrate_from_external_db.extract.dedicated_team_position_abilities_extractor import DedicatedTeamPositionAbilitiesExtractor
from second_eye_api.migrate_from_external_db.extract.project_team_position_abilities_extractor import ProjectTeamPositionAbilitiesExtractor
from second_eye_api.migrate_from_external_db.output_data import OutputData
from second_eye_api.migrate_from_external_db.load.skills_loader import SkillsLoader
from second_eye_api.migrate_from_external_db.load.systems_loader import SystemsLoader
from second_eye_api.migrate_from_external_db.load.dedicated_teams_loader import DedicatedTeamsLoader
from second_eye_api.migrate_from_external_db.load.project_teams_loader import ProjectTeamsLoader
from second_eye_api.migrate_from_external_db.load.change_requests_loader import ChangeRequestsLoader
from second_eye_api.migrate_from_external_db.load.system_change_requests_loader import SystemChangeRequestsLoader
from second_eye_api.migrate_from_external_db.load.tasks_loader import TasksLoader
from second_eye_api.migrate_from_external_db.load.persons_loader import PersonsLoader
from second_eye_api.migrate_from_external_db.load.dedicated_team_positions_loader import DedicatedTeamPositionsLoader
from second_eye_api.migrate_from_external_db.load.project_team_positions_loader import ProjectTeamPositionsLoader
from second_eye_api.migrate_from_external_db.load.dedicated_team_position_abilities_loader import DedicatedTeamPositionAbilitiesLoader
from second_eye_api.migrate_from_external_db.load.project_team_position_abilities_loader import ProjectTeamPositionAbilitiesLoader
from threading import Thread

def run_tasks_in_parallel(tasks):
    threads = [Thread(target=task) for task in tasks]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        print("{} done".format(thread))

def extract_input_data(get_connection, settings):
    input_data = InputData()

    skills_extractor = SkillsExtractor()
    systems_extractor = SystemsExtractor(get_connection=get_connection)
    dedicated_teams_extractor = DedicatedTeamsExtractor(get_connection=get_connection)
    project_teams_extractor = ProjectTeamsExtractor(get_connection=get_connection)
    change_requests_extractor = ChangeRequestsExtractor(get_connection=get_connection)
    system_change_requests_extractor = SystemChangeRequestsExtractor(get_connection=get_connection)
    tasks_extractor = TasksExtractor(get_connection=get_connection, last_period_number_of_days=settings.last_period_number_of_days)
    persons_extractor = PersonsExtractor(get_connection=get_connection)
    dedicated_team_positions_extractor = DedicatedTeamPositionsExtractor(get_connection=get_connection)
    project_team_positions_extractor = ProjectTeamPositionsExtractor(get_connection=get_connection)
    dedicated_team_position_abilities_extractor = DedicatedTeamPositionAbilitiesExtractor(get_connection=get_connection)
    project_team_position_abilities_extractor = ProjectTeamPositionAbilitiesExtractor(get_connection=get_connection)

    run_tasks_in_parallel([
        lambda: skills_extractor.extract(),
        lambda: systems_extractor.extract(),
        lambda: dedicated_teams_extractor.extract(),
        lambda: project_teams_extractor.extract(),
        lambda: change_requests_extractor.extract(),
        lambda: system_change_requests_extractor.extract(),
        lambda: tasks_extractor.extract(),
        lambda: persons_extractor.extract(),
        lambda: dedicated_team_positions_extractor.extract(),
        lambda: project_team_positions_extractor.extract(),
        lambda: dedicated_team_position_abilities_extractor.extract(),
        lambda: project_team_position_abilities_extractor.extract(),
    ])

    skills = skills_extractor.data
    input_data.skills = skills

    systems = systems_extractor.data
    input_data.systems = systems

    dedicated_teams = dedicated_teams_extractor.data
    input_data.dedicated_teams = dedicated_teams

    project_teams = project_teams_extractor.data
    input_data.project_teams = project_teams

    change_requests = change_requests_extractor.data
    input_data.change_requests = change_requests

    system_change_requests = system_change_requests_extractor.data
    input_data.system_change_requests = system_change_requests

    tasks = tasks_extractor.data
    input_data.tasks = tasks

    persons = persons_extractor.data
    input_data.persons = persons

    dedicated_team_positions = dedicated_team_positions_extractor.data
    input_data.dedicated_team_positions = dedicated_team_positions

    project_team_positions = project_team_positions_extractor.data
    input_data.project_team_positions = project_team_positions

    dedicated_team_position_abilities = dedicated_team_position_abilities_extractor.data
    input_data.dedicated_team_position_abilities = dedicated_team_position_abilities

    project_team_position_abilities = project_team_position_abilities_extractor.data
    input_data.project_team_position_abilities = project_team_position_abilities

    return input_data

def replace_column_values_with_minus_one_if_not_in_valid_list(dataframe, column_name, valid_list):
    dataframe.loc[~dataframe[column_name].isin(
        valid_list
    ), column_name] = -1

def replace_broken_system_change_request_change_request_id_to_change_request_id_with_minus_one(system_change_requests, change_requests):
    valid_change_request_ids = change_requests.reset_index()['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=system_change_requests,
        column_name="change_request_id",
        valid_list=valid_change_request_ids
    )

def replace_broken_task_system_change_request_id_to_system_change_request_id_with_minus_one(tasks, system_change_requests):
    valid_system_change_request_ids = system_change_requests.reset_index()['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=tasks,
        column_name="system_change_request_id",
        valid_list=valid_system_change_request_ids
    )

def replace_broken_dedicated_team_positions_person_id_to_persons_id_with_minus_one(dedicated_team_positions, persons):
    valid_person_ids = persons.reset_index()['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=dedicated_team_positions,
        column_name="person_id",
        valid_list=valid_person_ids
    )

def replace_broken_project_team_positions_person_id_to_persons_id_with_minus_one(project_team_positions, persons):
    valid_person_ids = persons.reset_index()['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=project_team_positions,
        column_name="person_id",
        valid_list=valid_person_ids
    )

def fix_broken_links(output_data):
    replace_broken_system_change_request_change_request_id_to_change_request_id_with_minus_one(
        system_change_requests=output_data.system_change_requests,
        change_requests=output_data.change_requests
    )

    replace_broken_task_system_change_request_id_to_system_change_request_id_with_minus_one(
        tasks=output_data.tasks,
        system_change_requests=output_data.system_change_requests
    )

    replace_broken_dedicated_team_positions_person_id_to_persons_id_with_minus_one(
        dedicated_team_positions=output_data.dedicated_team_positions,
        persons=output_data.persons
    )

    replace_broken_project_team_positions_person_id_to_persons_id_with_minus_one(
        project_team_positions=output_data.project_team_positions,
        persons=output_data.persons
    )

def transform_input_data_to_output_data(input_data, settings):
    output_data = OutputData()
    output_data.skills = input_data.skills
    output_data.systems = input_data.systems
    output_data.dedicated_teams = input_data.dedicated_teams
    output_data.project_teams = input_data.project_teams
    output_data.change_requests = input_data.change_requests
    output_data.system_change_requests = input_data.system_change_requests
    output_data.tasks = input_data.tasks
    output_data.persons = input_data.persons
    output_data.dedicated_team_positions = input_data.dedicated_team_positions
    output_data.project_team_positions = input_data.project_team_positions
    output_data.dedicated_team_position_abilities = input_data.dedicated_team_position_abilities
    output_data.project_team_position_abilities = input_data.project_team_position_abilities

    fix_broken_links(output_data=output_data)

    return output_data

def load_output_data(output_data, output_database):
    skills_loader = SkillsLoader(skills=output_data.skills, output_database=output_database)
    skills_loader.load()

    systems_loader = SystemsLoader(systems=output_data.systems, output_database=output_database)
    systems_loader.load()

    dedicated_teams_loader = DedicatedTeamsLoader(dedicated_teams=output_data.dedicated_teams, output_database=output_database)
    dedicated_teams_loader.load()

    project_teams_loader = ProjectTeamsLoader(project_teams=output_data.project_teams, output_database=output_database)
    project_teams_loader.load()

    change_requests_loader = ChangeRequestsLoader(change_requests=output_data.change_requests, output_database=output_database)
    change_requests_loader.load()

    system_change_requests_loader = SystemChangeRequestsLoader(system_change_requests=output_data.system_change_requests, output_database=output_database)
    system_change_requests_loader.load()

    tasks_loader = TasksLoader(tasks=output_data.tasks, output_database=output_database)
    tasks_loader.load()

    persons_loader = PersonsLoader(persons=output_data.persons, output_database=output_database)
    persons_loader.load()

    dedicated_team_positions_loader = DedicatedTeamPositionsLoader(dedicated_team_positions=output_data.dedicated_team_positions, output_database=output_database)
    dedicated_team_positions_loader.load()

    project_team_positions_loader = ProjectTeamPositionsLoader(project_team_positions=output_data.project_team_positions, output_database=output_database)
    project_team_positions_loader.load()

    dedicated_team_position_abilities_loader = DedicatedTeamPositionAbilitiesLoader(dedicated_team_position_abilities=output_data.dedicated_team_position_abilities, output_database=output_database)
    dedicated_team_position_abilities_loader.load()

    project_team_position_abilities_loader = ProjectTeamPositionAbilitiesLoader(project_team_position_abilities=output_data.project_team_position_abilities, output_database=output_database)
    project_team_position_abilities_loader.load()

def migrate(get_input_connection, output_database, settings):
    print("extract")
    input_data = extract_input_data(
        get_connection=get_input_connection,
        settings=settings
    )

    print("transform")
    output_data = transform_input_data_to_output_data(input_data=input_data, settings=settings)

    print("load")
    load_output_data(output_data=output_data, output_database=output_database)

    print("done")