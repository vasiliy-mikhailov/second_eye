def calculate_task_time_sheets_by_date(task_time_sheets):
    result = task_time_sheets.copy()
    result = result[["task_id", "date", "time_spent"]].groupby(
        ["task_id", "date"]
    ).agg({"time_spent": "sum"}).reset_index()
    result = task_time_sheets[["task_id", "date", "time_spent"]].sort_values(["date"]).reset_index(drop=True)
    result["time_spent_cumsum"] = result.groupby(["task_id"])["time_spent"].cumsum(axis=0)

    return result