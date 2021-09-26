from .utils import *
from .state import StateCategory
import pandas as pd

def make_filler_system_change_requests_summing_up_to_change_request_estimate(system_change_requests, change_requests):
    system_change_requests["is_filler"] = False

    change_requests_dont_having_enough_change_requests = change_requests[change_requests["estimate"] > change_requests["system_change_requests_estimate_sum"]]

    additional_system_change_requests = change_requests_dont_having_enough_change_requests[[
        "id",
        "estimate",
        "system_change_requests_estimate_sum",
        "analysis_estimate",
        "system_change_requests_analysis_estimate_sum",
        "development_estimate",
        "system_change_requests_development_estimate_sum",
        "testing_estimate",
        "system_change_requests_testing_estimate_sum"
    ]].copy()

    additional_system_change_requests["estimate"] = additional_system_change_requests["estimate"] - additional_system_change_requests["system_change_requests_estimate_sum"]
    additional_system_change_requests["analysis_estimate"] = additional_system_change_requests["analysis_estimate"] - additional_system_change_requests["system_change_requests_analysis_estimate_sum"]
    additional_system_change_requests["development_estimate"] = additional_system_change_requests["development_estimate"] - additional_system_change_requests["system_change_requests_development_estimate_sum"]
    additional_system_change_requests["testing_estimate"] = additional_system_change_requests["testing_estimate"] - additional_system_change_requests["system_change_requests_testing_estimate_sum"]
    additional_system_change_requests.rename(columns={"id": "change_request_id"}, inplace=True)
    additional_system_change_requests.drop(
        labels=[
            "system_change_requests_estimate_sum",
            "system_change_requests_analysis_estimate_sum",
            "system_change_requests_development_estimate_sum",
            "system_change_requests_testing_estimate_sum"
        ],
        axis=1,
        inplace=True
    )
    additional_system_change_requests["url"] = "https://none.com"
    additional_system_change_requests["name"] = "Заполнитель"
    additional_system_change_requests["system_id"] = -1
    additional_system_change_requests["analysis_preliminary_estimate"] = additional_system_change_requests["analysis_estimate"]
    additional_system_change_requests["development_preliminary_estimate"] = additional_system_change_requests["development_estimate"]
    additional_system_change_requests["testing_preliminary_estimate"] = additional_system_change_requests["testing_estimate"]
    additional_system_change_requests["analysis_planned_estimate"] = additional_system_change_requests["analysis_estimate"]
    additional_system_change_requests["development_planned_estimate"] = additional_system_change_requests["development_estimate"]
    additional_system_change_requests["testing_planned_estimate"] = additional_system_change_requests["testing_estimate"]
    additional_system_change_requests["state_id"] = "-1"
    additional_system_change_requests["state_category_id"] = StateCategory.TODO
    additional_system_change_requests["analysis_tasks_estimate_sum"] = 0
    additional_system_change_requests["development_tasks_estimate_sum"] = 0
    additional_system_change_requests["testing_tasks_estimate_sum"] = 0
    additional_system_change_requests["tasks_estimate_sum"] = 0
    additional_system_change_requests["analysis_time_spent"] = 0
    additional_system_change_requests["development_time_spent"] = 0
    additional_system_change_requests["testing_time_spent"] = 0
    additional_system_change_requests["time_spent"] = 0
    additional_system_change_requests["analysis_time_left"] = additional_system_change_requests["analysis_estimate"]
    additional_system_change_requests["development_time_left"] = additional_system_change_requests["development_estimate"]
    additional_system_change_requests["testing_time_left"] = additional_system_change_requests["testing_estimate"]
    additional_system_change_requests["time_left"] = additional_system_change_requests["estimate"]
    additional_system_change_requests["is_filler"] = True

    system_change_requests = system_change_requests.append(
        additional_system_change_requests,
        sort=False)

    system_change_requests.reset_index(inplace=True, drop=True)  # to prevent duplicate row names

    system_change_requests["id"] = system_change_requests.apply(lambda x:
        -x.name - 1 if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return system_change_requests