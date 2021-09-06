from second_eye_api.migrate_from_external_db.transform.utils import *
from second_eye_api.schema.state_category import StateCategory
from second_eye_api.schema.skill import Skill
import pandas as pd

def make_filler_analysis_tasks_summing_up_to_system_change_request_analysis_estimate(tasks, system_change_requests):
    system_change_requests_dont_having_enough_analysis_tasks = system_change_requests[
        system_change_requests["analysis_estimate"] > system_change_requests["analysis_tasks_estimate_sum"]]

    additional_tasks = system_change_requests_dont_having_enough_analysis_tasks[[
        "id",
        "analysis_tasks_estimate_sum",
        "analysis_estimate",
        "system_id"
    ]].copy()

    additional_tasks["estimate"] = additional_tasks["analysis_estimate"] - additional_tasks["analysis_tasks_estimate_sum"]
    additional_tasks.rename(columns={"id": "system_change_request_id"}, inplace=True)
    additional_tasks.drop(
        labels=[
            "analysis_tasks_estimate_sum",
            "analysis_estimate"
        ],
        axis=1,
        inplace=True
    )
    additional_tasks["url"] = "https://none.com"
    additional_tasks["name"] = "Заполнитель"
    additional_tasks["skill_id"] = Skill.ANALYSIS
    additional_tasks["system_id"] = -1
    additional_tasks["preliminary_estimate"] = additional_tasks["estimate"]
    additional_tasks["planned_estimate"] = additional_tasks["estimate"]
    additional_tasks["time_spent"] = 0
    additional_tasks["state_id"] = "-1"
    additional_tasks["state_category_id"] = StateCategory.TODO
    additional_tasks["time_left"] = additional_tasks["estimate"]
    additional_tasks["is_filler"] = True

    tasks = tasks.append(
        additional_tasks,
        sort=False)

    tasks.reset_index(inplace=True, drop=True) # to prevent duplicate row names

    tasks["id"] = tasks.apply(lambda x:
        str(-x.name - 1) if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return tasks

def make_filler_development_tasks_summing_up_to_system_change_request_development_estimate(tasks, system_change_requests):
    system_change_requests_dont_having_enough_development_tasks = system_change_requests[
        system_change_requests["development_estimate"] > system_change_requests["development_tasks_estimate_sum"]]

    additional_tasks = system_change_requests_dont_having_enough_development_tasks[[
        "id",
        "development_tasks_estimate_sum",
        "development_estimate",
        "system_id"
    ]].copy()

    additional_tasks["estimate"] = additional_tasks["development_estimate"] - additional_tasks["development_tasks_estimate_sum"]
    additional_tasks.rename(columns={"id": "system_change_request_id"}, inplace=True)
    additional_tasks.drop(
        labels=[
            "development_tasks_estimate_sum",
            "development_estimate"
        ],
        axis=1,
        inplace=True
    )
    additional_tasks["url"] = "https://none.com"
    additional_tasks["name"] = "Заполнитель"
    additional_tasks["skill_id"] = Skill.DEVELOPMENT
    additional_tasks["system_id"] = -1
    additional_tasks["preliminary_estimate"] = additional_tasks["estimate"]
    additional_tasks["planned_estimate"] = additional_tasks["estimate"]
    additional_tasks["time_spent"] = 0
    additional_tasks["state_id"] = "-1"
    additional_tasks["state_category_id"] = StateCategory.TODO
    additional_tasks["time_left"] = additional_tasks["estimate"]
    additional_tasks["is_filler"] = True

    tasks = tasks.append(
        additional_tasks,
        sort=False)

    tasks.reset_index(inplace=True, drop=True) # to prevent duplicate row names

    tasks["id"] = tasks.apply(lambda x:
        str(-x.name - 1) if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return tasks

def make_filler_testing_tasks_summing_up_to_system_change_request_testing_estimate(tasks, system_change_requests):
    system_change_requests_dont_having_enough_testing_tasks = system_change_requests[
        system_change_requests["testing_estimate"] > system_change_requests["testing_tasks_estimate_sum"]]

    additional_tasks = system_change_requests_dont_having_enough_testing_tasks[[
        "id",
        "testing_tasks_estimate_sum",
        "testing_estimate",
        "system_id"
    ]].copy()

    additional_tasks["estimate"] = additional_tasks["testing_estimate"] - additional_tasks["testing_tasks_estimate_sum"]
    additional_tasks.rename(columns={"id": "system_change_request_id"}, inplace=True)
    additional_tasks.drop(
        labels=[
            "testing_tasks_estimate_sum",
            "testing_estimate"
        ],
        axis=1,
        inplace=True
    )
    additional_tasks["url"] = "https://none.com"
    additional_tasks["name"] = "Заполнитель"
    additional_tasks["skill_id"] = Skill.TESTING
    additional_tasks["system_id"] = -1
    additional_tasks["preliminary_estimate"] = additional_tasks["estimate"]
    additional_tasks["planned_estimate"] = additional_tasks["estimate"]
    additional_tasks["time_spent"] = 0
    additional_tasks["state_id"] = "-1"
    additional_tasks["state_category_id"] = StateCategory.TODO
    additional_tasks["time_left"] = additional_tasks["estimate"]
    additional_tasks["is_filler"] = True

    tasks = tasks.append(
        additional_tasks,
        sort=False)

    tasks.reset_index(inplace=True, drop=True) # to prevent duplicate row names

    tasks["id"] = tasks.apply(lambda x:
        str(-x.name - 1) if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return tasks

def make_filler_tasks_summing_up_to_system_change_request_estimate(tasks, system_change_requests):
    tasks["is_filler"] = False

    tasks = make_filler_analysis_tasks_summing_up_to_system_change_request_analysis_estimate(
        tasks=tasks,
        system_change_requests=system_change_requests
    )

    tasks = make_filler_development_tasks_summing_up_to_system_change_request_development_estimate(
        tasks=tasks,
        system_change_requests=system_change_requests
    )

    tasks = make_filler_testing_tasks_summing_up_to_system_change_request_testing_estimate(
        tasks=tasks,
        system_change_requests=system_change_requests
    )

    return tasks
