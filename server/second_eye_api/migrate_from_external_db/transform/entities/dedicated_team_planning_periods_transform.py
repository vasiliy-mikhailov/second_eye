def calculate_dedicated_team_planning_periods_from_change_requests_planning_period_id_and_dedicated_team(change_requests):
    result = change_requests.groupby(["planning_period_id", "dedicated_team_id"]).size().reset_index(name="count")
    result["id"] = result.apply(lambda x:
        -1 if x["planning_period_id"] == -1 and x["dedicated_team_id"] == -1 else x.name + 1,
        axis=1
    )
    return result

def calculate_dedicated_team_planning_periods_estimate_by_tasks_estimate(dedicated_team_planning_periods, tasks):
    tasks_estimate_aggregated_by_dedicated_team_id_and_planning_period_id = tasks.groupby(
        ["dedicated_team_id", "planning_period_id"]
    ).agg({
        "estimate": "sum"
    })

    dedicated_team_planning_periods = dedicated_team_planning_periods.merge(
        tasks_estimate_aggregated_by_dedicated_team_id_and_planning_period_id,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    dedicated_team_planning_periods["estimate"].fillna(0, inplace=True)

    return dedicated_team_planning_periods

def calculate_dedicated_team_planning_periods_time_spent_by_tasks_time_spent(dedicated_team_planning_periods, tasks):
    tasks_time_spent_aggregated_by_dedicated_team_id_and_planning_period_id = tasks.groupby(
        ["dedicated_team_id", "planning_period_id"]
    ).agg({
        "time_spent": "sum"
    })

    dedicated_team_planning_periods = dedicated_team_planning_periods.merge(
        tasks_time_spent_aggregated_by_dedicated_team_id_and_planning_period_id,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    dedicated_team_planning_periods["time_spent"].fillna(0, inplace=True)

    return dedicated_team_planning_periods

def calculate_dedicated_team_planning_periods_time_left_by_tasks_time_left(dedicated_team_planning_periods, tasks):
    tasks_time_left_aggregated_by_dedicated_team_id_and_planning_period_id = tasks.groupby(
        ["dedicated_team_id", "planning_period_id"]
    ).agg({
        "time_left": "sum"
    })

    dedicated_team_planning_periods = dedicated_team_planning_periods.merge(
        tasks_time_left_aggregated_by_dedicated_team_id_and_planning_period_id,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    dedicated_team_planning_periods["time_left"].fillna(0, inplace=True)

    return dedicated_team_planning_periods