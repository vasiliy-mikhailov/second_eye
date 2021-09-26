import pandas as pd
import numpy as np
from .skill import Skill
from datetime import datetime, date, timedelta

def replace_column_values_with_minus_one_if_not_in_valid_list(dataframe, column_name, valid_list):
    dataframe.loc[~dataframe[column_name].isin(
        valid_list
    ), column_name] = -1

def calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
    entities,
    task_time_sheets,
    sum_up_by_column,
    skill
):
    time_spent_last_period_column_names = {
        Skill.ANALYSIS: "analysis_time_spent_last_period",
        Skill.DEVELOPMENT: "development_time_spent_last_period",
        Skill.TESTING: "testing_time_spent_last_period"
    }

    actual_capacity_column_names = {
        Skill.ANALYSIS: "actual_analysis_capacity",
        Skill.DEVELOPMENT: "actual_development_capacity",
        Skill.TESTING: "actual_testing_capacity"
    }

    time_spent_last_period_column_name = "time_spent_last_period" if not skill else time_spent_last_period_column_names[
        skill
    ]

    number_of_days_in_period = 28
    skip_days = 7
    work_days = 5
    week_days = 7
    today = datetime.now().date()
    start = today - timedelta(days=number_of_days_in_period + skip_days)
    end = today - timedelta(days=skip_days)

    tasks_time_sheets_filtered_by_skill = task_time_sheets if not skill else task_time_sheets[
        task_time_sheets["skill_id"] == skill
    ]

    task_time_sheets_behind = tasks_time_sheets_filtered_by_skill[
        (task_time_sheets["date"] >= start)
        & (task_time_sheets["date"] < end)
    ].copy()

    tasks_time_sheets_aggregated_by_company_id = task_time_sheets_behind.groupby(
        [sum_up_by_column]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            sum_up_by_column: "id",
            "time_spent": time_spent_last_period_column_name
        },
    )

    entities = entities.merge(
        tasks_time_sheets_aggregated_by_company_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    entities[time_spent_last_period_column_name].fillna(0, inplace=True)

    actual_capacity_column_name = "actual_change_request_capacity" if not skill else actual_capacity_column_names[
        skill
    ]

    entities[actual_capacity_column_name] = entities[time_spent_last_period_column_name] / number_of_days_in_period * week_days / work_days

    return entities

def calculate_entities_actual_change_request_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=None
    )

def calculate_entities_actual_analysis_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.ANALYSIS
    )


def calculate_entities_actual_development_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.DEVELOPMENT
    )


def calculate_entities_actual_testing_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.TESTING
    )

def linear_polyfit(x, y):
    try:
        non_nan_indexes = np.isfinite(x) & np.isfinite(y)
        non_nan_x, non_nan_y = x[non_nan_indexes], y[non_nan_indexes]
        result = np.polyfit(non_nan_x, non_nan_y, 1, w=y).tolist()
        return result
    except:
        return [float("nan"), float("nan")]

def normalize(x, min_x, max_x):
    if not pd.isnull(min_x) and not pd.isnull(max_x) and min_x != max_x:
        return (x - min_x) / (max_x - min_x)
    else:
        return 0
