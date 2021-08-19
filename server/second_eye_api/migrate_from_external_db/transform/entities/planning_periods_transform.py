import pandas as pd

def calculate_planning_periods_name_using_id_inplace(planning_periods):
    planning_periods['name'] = planning_periods.apply(lambda x:
        str(x['id']) if x['id'] != -1 else 'Не указано', axis=1
    )

def calculate_planning_periods_start_using_id_inplace(planning_periods):
    planning_periods['start'] = planning_periods.apply(lambda x:
       "{:04d}-01-01".format(x['id']) if x['id'] != -1 else '2100-01-01',
        axis=1
    )

def calculate_planning_periods_end_using_id_inplace(planning_periods):
    planning_periods['end'] = planning_periods.apply(lambda x:
        "{:04d}-12-31".format(x['id']) if x['id'] != -1 else '2100-12-31',
        axis=1
    )

def calculate_planning_periods_estimate_using_tasks_estimate(planning_periods, tasks):
    tasks_estimate_aggregated_by_planning_period_id = tasks.groupby(
        ["planning_period_id"]
    ).agg({
        "estimate": "sum"
    })

    tasks_estimate_aggregated_by_planning_period_id.rename(columns={
        "planning_period_id": "id",
    }, inplace=True)

    planning_periods = planning_periods.merge(
        tasks_estimate_aggregated_by_planning_period_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    planning_periods["estimate"].fillna(0, inplace=True)

    return planning_periods

def calculate_planning_periods_time_spent_using_tasks_time_spent(planning_periods, tasks):
    tasks_time_spent_aggregated_by_planning_period_id = tasks.groupby(
        ["planning_period_id"]
    ).agg({
        "time_spent": "sum"
    })

    tasks_time_spent_aggregated_by_planning_period_id.rename(columns={
        "planning_period_id": "id",
    }, inplace=True)

    planning_periods = planning_periods.merge(
        tasks_time_spent_aggregated_by_planning_period_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    planning_periods["time_spent"].fillna(0, inplace=True)

    return planning_periods

def calculate_planning_periods_time_left_using_tasks_time_left(planning_periods, tasks):
    tasks_time_left_aggregated_by_planning_period_id = tasks.groupby(
        ["planning_period_id"]
    ).agg({
        "time_left": "sum"
    })

    tasks_time_left_aggregated_by_planning_period_id.rename(columns={
        "planning_period_id": "id",
    }, inplace=True)

    planning_periods = planning_periods.merge(
        tasks_time_left_aggregated_by_planning_period_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    planning_periods["time_left"].fillna(0, inplace=True)

    return planning_periods