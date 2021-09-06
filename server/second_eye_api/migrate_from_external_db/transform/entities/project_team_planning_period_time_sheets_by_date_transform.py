from ..utils import normalize
import pandas as pd

def propagate_project_team_planning_period_planning_period_start_into_project_team_planning_period_time_sheets_by_date(
        project_team_planning_period_time_sheets_by_date,
        project_team_planning_periods
):
    project_team_planning_periods_reduced_to_id_and_start = project_team_planning_periods[["id", "planning_period_start"]].rename(columns={
        "id": "project_team_planning_period_id",
    })

    return project_team_planning_period_time_sheets_by_date.merge(
        project_team_planning_periods_reduced_to_id_and_start,
        how="left",
        on="project_team_planning_period_id",
        suffixes=(None, ""),
    )

def propagate_project_team_planning_period_planning_period_end_into_project_team_planning_period_time_sheets_by_date(
        project_team_planning_period_time_sheets_by_date,
        project_team_planning_periods
):
    planning_periods_reduced_to_id_and_start = project_team_planning_periods[["id", "planning_period_end"]].rename(columns={
        "id": "project_team_planning_period_id",
    })

    return project_team_planning_period_time_sheets_by_date.merge(
        planning_periods_reduced_to_id_and_start,
        how="left",
        on="project_team_planning_period_id",
        suffixes=(None, ""),
    )

def calculate_project_team_planning_period_time_spent_cumsum_prediction_by_project_team_planning_periods_m_and_b(
        project_team_planning_period_time_sheets_by_date,
        project_team_planning_periods
):
    project_team_planning_periods_reduced_to_id_m_and_b = project_team_planning_periods[["id", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]]
    project_team_planning_periods_reduced_to_id_m_and_b.set_index("id", inplace=True)


    result = project_team_planning_period_time_sheets_by_date.merge(
        project_team_planning_periods_reduced_to_id_m_and_b,
        how="left",
        left_on="project_team_planning_period_id",
        right_index=True,
        suffixes=(None, "")
    )

    result["time_spent_cumsum_prediction"] = result.apply(lambda x:
        normalize(x=x["date"], min_x=x["planning_period_start"], max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
        axis=1
    )

    return result