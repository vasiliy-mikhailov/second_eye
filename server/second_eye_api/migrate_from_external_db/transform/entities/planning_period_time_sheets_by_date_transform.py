def calculate_planning_period_time_sheets_by_date(task_time_sheets):
    result = task_time_sheets.copy()
    result = result[["planning_period_id", "date", "time_spent"]].groupby(
        ["planning_period_id", "date"]
    ).agg({"time_spent": "sum"}).reset_index()
    result = result.sort_values(["date"]).reset_index(drop=True)
    result["time_spent_cumsum"] = result.groupby(["planning_period_id"])["time_spent"].cumsum(axis=0)

    return result