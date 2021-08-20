def calculate_project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date(task_time_sheets):
    result = task_time_sheets.copy()

    result["time_spent_with_value"] = result.apply(lambda x:
        x["time_spent"] if x["has_value"] else 0,
        axis=1
    )

    result["time_spent_without_value"] = result.apply(lambda x:
        x["time_spent"] if not x["has_value"] else 0,
        axis=1
    )

    result = result[["project_team_planning_period_id", "date", "time_spent", "time_spent_with_value", "time_spent_without_value"]].groupby(
        ["project_team_planning_period_id", "date"]
    ).agg({"time_spent_with_value": "sum", "time_spent_without_value": "sum"}).reset_index()
    result = result.sort_values(["date"]).reset_index(drop=True)

    result["time_spent_with_value_cumsum"] = result.groupby(["project_team_planning_period_id"])["time_spent_with_value"].cumsum(axis=0)
    result["time_spent_without_value_cumsum"] = result.groupby(["project_team_planning_period_id"])["time_spent_without_value"].cumsum(axis=0)
    result["time_spent_cumsum"] = result["time_spent_without_value_cumsum"] + result["time_spent_with_value_cumsum"]

    result["time_spent_with_value_percent_cumsum"] = result.apply(lambda x:
        1 if x["time_spent_cumsum"] == 0 else x["time_spent_with_value_cumsum"] / x["time_spent_cumsum"],
        axis=1
    )

    result["time_spent_without_value_percent_cumsum"] = result.apply(lambda x:
        0 if x["time_spent_cumsum"] == 0 else x["time_spent_without_value_cumsum"] / x["time_spent_cumsum"],
        axis=1
    )

    result = result[["project_team_planning_period_id", "date", "time_spent_with_value_percent_cumsum", "time_spent_without_value_percent_cumsum"]]

    return result