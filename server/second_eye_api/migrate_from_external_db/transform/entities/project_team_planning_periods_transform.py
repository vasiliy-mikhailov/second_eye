def calculate_project_team_planning_periods_from_change_requests_planning_period_id_and_project_team_id(change_requests):
    result = change_requests.groupby(["dedicated_team_id", "planning_period_id", "project_team_id"]).size().reset_index(name="count")
    result["id"] = result.apply(lambda x:
        -1 if x["planning_period_id"] == -1 and x["project_team_id"] == -1 else x.name + 1,
        axis=1
    )
    return result

def calculate_project_team_planning_periods_estimate_by_tasks_estimate(project_team_planning_periods, tasks):
    tasks_estimate_aggregated_by_project_team_id_and_planning_period_id = tasks.groupby(
        ["project_team_id", "planning_period_id"]
    ).agg({
        "estimate": "sum"
    })

    project_team_planning_periods = project_team_planning_periods.merge(
        tasks_estimate_aggregated_by_project_team_id_and_planning_period_id,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    project_team_planning_periods["estimate"].fillna(0, inplace=True)

    return project_team_planning_periods

def calculate_project_team_planning_periods_time_spent_by_tasks_time_spent(project_team_planning_periods, tasks):
    tasks_time_spent_aggregated_by_project_team_id_and_planning_period_id = tasks.groupby(
        ["project_team_id", "planning_period_id"]
    ).agg({
        "time_spent": "sum"
    })

    project_team_planning_periods = project_team_planning_periods.merge(
        tasks_time_spent_aggregated_by_project_team_id_and_planning_period_id,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    project_team_planning_periods["time_spent"].fillna(0, inplace=True)

    return project_team_planning_periods

def calculate_project_team_planning_periods_time_left_by_tasks_time_left(project_team_planning_periods, tasks):
    tasks_time_left_aggregated_by_project_team_id_and_planning_period_id = tasks.groupby(
        ["project_team_id", "planning_period_id"]
    ).agg({
        "time_left": "sum"
    })

    project_team_planning_periods = project_team_planning_periods.merge(
        tasks_time_left_aggregated_by_project_team_id_and_planning_period_id,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    project_team_planning_periods["time_left"].fillna(0, inplace=True)

    return project_team_planning_periods

def propagate_dedicated_team_planning_period_id_by_dedicated_team_id_and_planning_period_id_into_project_team_planning_periods(
        project_team_planning_periods,
        dedicated_team_planning_periods
):
    dedicated_team_id_and_planning_period_id_to_dedicated_team_planning_period_id_id_mapping = dedicated_team_planning_periods[
        ["id", "dedicated_team_id", "planning_period_id"]].rename(columns={"id": "dedicated_team_planning_period_id"})

    return project_team_planning_periods.merge(
        dedicated_team_id_and_planning_period_id_to_dedicated_team_planning_period_id_id_mapping,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(None, ""),
    )