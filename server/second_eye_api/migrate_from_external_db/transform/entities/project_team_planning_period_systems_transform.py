import pandas as pd
from ..utils import linear_polyfit

def calculate_project_team_planning_period_systems_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
    project_team_planning_period_systems,
    project_team_planning_period_system_time_sheets_by_date,
):
    project_team_planning_period_system_task_time_sheets_filtered_by_period_start_and_end = project_team_planning_period_system_time_sheets_by_date[
        (project_team_planning_period_system_time_sheets_by_date["date"] >= project_team_planning_period_system_time_sheets_by_date["planning_period_start"])
        & (project_team_planning_period_system_time_sheets_by_date["date"] <= project_team_planning_period_system_time_sheets_by_date["planning_period_end"])
    ]
    model = project_team_planning_period_system_task_time_sheets_filtered_by_period_start_and_end.groupby(
        ["project_team_planning_period_system_id"]
    ).apply(lambda x: pd.Series(
        linear_polyfit(
            x=(x["date"] - x["planning_period_start"]) / (x["planning_period_end"] - x["planning_period_start"]),
            y=x["time_spent_cumsum"]),
        index=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
    ))

    result = project_team_planning_period_systems.merge(
        model,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, "")
    )

    return result

def calculate_project_team_planning_period_system_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        project_team_planning_period_systems
):
    project_team_planning_period_systems["time_spent_cumsum_at_end_prediction"] = 1 * project_team_planning_period_systems["time_sheets_by_date_model_m"] + project_team_planning_period_systems["time_sheets_by_date_model_b"]