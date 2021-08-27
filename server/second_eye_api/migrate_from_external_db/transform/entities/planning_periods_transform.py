import pandas as pd
import datetime
from ..utils import linear_polyfit

def calculate_planning_periods_name_using_id_inplace(planning_periods):
    planning_periods['name'] = planning_periods.apply(lambda x:
        str(x['id']) if x['id'] != -1 else 'Не указано', axis=1
    )

def calculate_planning_periods_start_using_id_inplace(planning_periods):
    planning_periods['start'] = planning_periods.apply(lambda x:
        datetime.date(x['id'], 1, 1) if x['id'] != -1 else datetime.date(2100, 1, 1),
        axis=1
    )

def calculate_planning_periods_end_using_id_inplace(planning_periods):
    planning_periods['end'] = planning_periods.apply(lambda x:
        datetime.date(x['id'], 12, 31) if x['id'] != -1 else datetime.date(2100, 12, 31),
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

def calculate_planning_periods_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
    planning_periods,
    planning_period_time_sheets_by_date,
):
    planning_period_task_time_sheets_filtered_by_period_start_and_end = planning_period_time_sheets_by_date[
        (planning_period_time_sheets_by_date["date"] >= planning_period_time_sheets_by_date["planning_period_start"])
        & (planning_period_time_sheets_by_date["date"] <= planning_period_time_sheets_by_date["planning_period_end"])
    ]
    model = planning_period_task_time_sheets_filtered_by_period_start_and_end.groupby(
        ["planning_period_id"]
    ).apply(lambda x: pd.Series(
        linear_polyfit(
            x=(x["date"] - x["planning_period_start"]) / (x["planning_period_end"] - x["planning_period_start"]),
            y=x["time_spent_cumsum"]),
        index=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
    ))

    result = planning_periods.merge(
        model,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, "")
    )

    return result

def calculate_planning_period_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        planning_periods
):
    planning_periods["time_spent_cumsum_at_end_prediction"] = 1 * planning_periods["time_sheets_by_date_model_m"] + planning_periods["time_sheets_by_date_model_b"]
