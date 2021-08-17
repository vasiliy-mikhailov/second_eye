from second_eye_api.models import Skill

def calculate_change_request_analysis_time_sheets_by_date(task_time_sheets):
    result = task_time_sheets[task_time_sheets["skill_id"] == Skill.ANALYSIS].copy()
    result = result[["change_request_id", "date", "time_spent"]].groupby(
        ["change_request_id", "date"]
    ).agg({"time_spent": "sum"}).reset_index()
    result = result.sort_values(["date"]).reset_index(drop=True)
    result["time_spent_cumsum"] = result.groupby(["change_request_id"])["time_spent"].cumsum(axis=0)

    return result

def calculate_change_request_development_time_sheets_by_date(task_time_sheets):
    result = task_time_sheets[task_time_sheets["skill_id"] == Skill.DEVELOPMENT].copy()
    result = result[["change_request_id", "date", "time_spent"]].groupby(
        ["change_request_id", "date"]
    ).agg({"time_spent": "sum"}).reset_index()
    result = result.sort_values(["date"]).reset_index(drop=True)
    result["time_spent_cumsum"] = result.groupby(["change_request_id"])["time_spent"].cumsum(axis=0)

    return result

def calculate_change_request_testing_time_sheets_by_date(task_time_sheets):
    result = task_time_sheets[task_time_sheets["skill_id"] == Skill.TESTING].copy()
    result = result[["change_request_id", "date", "time_spent"]].groupby(
        ["change_request_id", "date"]
    ).agg({"time_spent": "sum"}).reset_index()
    result = result.sort_values(["date"]).reset_index(drop=True)
    result["time_spent_cumsum"] = result.groupby(["change_request_id"])["time_spent"].cumsum(axis=0)

    return result

def calculate_change_request_time_sheets_by_date(task_time_sheets):
    result = task_time_sheets.copy()
    result = result[["change_request_id", "date", "time_spent"]].groupby(
        ["change_request_id", "date"]
    ).agg({"time_spent": "sum"}).reset_index()
    result = result.sort_values(["date"]).reset_index(drop=True)
    result["time_spent_cumsum"] = result.groupby(["change_request_id"])["time_spent"].cumsum(axis=0)

    return result