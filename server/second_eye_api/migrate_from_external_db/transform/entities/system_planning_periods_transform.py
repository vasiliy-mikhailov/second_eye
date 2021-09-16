import pandas as pd
from ..utils import linear_polyfit

def calculate_system_planning_periods_development_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
    system_planning_periods,
    system_planning_period_development_time_sheets_by_date,
):
    system_planning_period_task_time_sheets_filtered_by_period_start_and_end = system_planning_period_development_time_sheets_by_date[
        (system_planning_period_development_time_sheets_by_date["date"] >= system_planning_period_development_time_sheets_by_date["planning_period_start"])
        & (system_planning_period_development_time_sheets_by_date["date"] <= system_planning_period_development_time_sheets_by_date["planning_period_end"])
    ]
    model = system_planning_period_task_time_sheets_filtered_by_period_start_and_end.groupby(
        ["system_planning_period_id"]
    ).apply(lambda x: pd.Series(
        linear_polyfit(
            x=(x["date"] - x["planning_period_start"]) / (x["planning_period_end"] - x["planning_period_start"]),
            y=x["time_spent_cumsum"]),
        index=["development_time_sheets_by_date_model_m", "development_time_sheets_by_date_model_b"]
    ))

    result = system_planning_periods.merge(
        model,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, "")
    )

    return result

def calculate_system_planning_period_development_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        system_planning_periods
):
    system_planning_periods["development_time_spent_cumsum_at_end_prediction"] = 1 * system_planning_periods["development_time_sheets_by_date_model_m"] + system_planning_periods["development_time_sheets_by_date_model_b"]

def calculate_system_planning_periods_testing_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
    system_planning_periods,
    system_planning_period_testing_time_sheets_by_date,
):
    system_planning_period_task_time_sheets_filtered_by_period_start_and_end = system_planning_period_testing_time_sheets_by_date[
        (system_planning_period_testing_time_sheets_by_date["date"] >= system_planning_period_testing_time_sheets_by_date["planning_period_start"])
        & (system_planning_period_testing_time_sheets_by_date["date"] <= system_planning_period_testing_time_sheets_by_date["planning_period_end"])
    ]
    model = system_planning_period_task_time_sheets_filtered_by_period_start_and_end.groupby(
        ["system_planning_period_id"]
    ).apply(lambda x: pd.Series(
        linear_polyfit(
            x=(x["date"] - x["planning_period_start"]) / (x["planning_period_end"] - x["planning_period_start"]),
            y=x["time_spent_cumsum"]),
        index=["testing_time_sheets_by_date_model_m", "testing_time_sheets_by_date_model_b"]
    ))

    result = system_planning_periods.merge(
        model,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, "")
    )

    return result

def calculate_system_planning_period_testing_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        system_planning_periods
):
    system_planning_periods["testing_time_spent_cumsum_at_end_prediction"] = 1 * system_planning_periods["testing_time_sheets_by_date_model_m"] + system_planning_periods["testing_time_sheets_by_date_model_b"]