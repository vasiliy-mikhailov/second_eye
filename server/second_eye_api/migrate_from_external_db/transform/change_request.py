import datetime
import cubista
import pandas as pd

from . import change_request
from . import dedicated_team_planning_period
from . import dedicated_team_quarter
from . import epic
from . import field_pack
from . import planning_period
from . import project_team
from . import project_team_planning_period
from . import project_team_quarter
from . import quarter
from . import state
from . import system_change_request
from . import time_sheet
from . import utils

class ChangeRequest(cubista.Table):
    CHANGE_REQUESTS_WITHOUT_FUNCTION_POINTS = [
        "MKB-23539"
    ]

    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        analysis_express_estimate = cubista.FloatField(nulls=True)
        development_express_estimate = cubista.FloatField(nulls=True)
        testing_express_estimate = cubista.FloatField(nulls=True)
        quarter_key = cubista.StringField()
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["id"],
            source_fields=["id"]
        )

        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default="-1", nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        planned_install_date = cubista.DateField(nulls=True)
        year_label_max = cubista.IntField(nulls=True)
        has_value = cubista.IntField()
        is_reengineering = cubista.IntField()
        project_team_id = cubista.ForeignKeyField(foreign_table=lambda: project_team.ProjectTeam, default=-1, nulls=False)
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="project_manager_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="dedicated_team_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="company_id")
        epic_id = cubista.ForeignKeyField(foreign_table=lambda: epic.Epic, default=-1, nulls=False)

        express_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_express_estimate"] + x["development_express_estimate"] + x["testing_express_estimate"],
            source_fields=["analysis_express_estimate", "development_express_estimate", "testing_express_estimate"]
        )

        quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_key"],
            foreign_field_names=["key"],
            pulled_field_name="id",
            default=-1
        )

        quarter_start = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.date.today()
        )

        quarter_end = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.date.today()
        )

        quarter_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_id_as_specified_in_source = cubista.CalculatedField(
            lambda_expression=lambda x: x["install_date"].year if not pd.isnull(x["install_date"]) else (
                x["resolution_date"].year if not pd.isnull(x["resolution_date"]) and x["state_category_id"] == state.StateCategory.DONE else (
                    x["planned_install_date"].year if not pd.isnull(x["planned_install_date"]) else (
                        x["quarter_planning_period_id"] if x["quarter_id"] != -1 else (
                            x["year_label_max"] if x["year_label_max"] != -1 else -1
                        )
                    )
                )
            ),
            source_fields=["install_date", "resolution_date", "state_category_id", "planned_install_date", "year_label_max", "quarter_planning_period_id", "quarter_id"]
        )

        planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: utils.get_current_year() if x["state_category_id"] != state.StateCategory.DONE and x["planning_period_id_as_specified_in_source"] > -1 else x["planning_period_id_as_specified_in_source"],
            source_fields=["state_category_id", "planning_period_id_as_specified_in_source"]
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.date.today()
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.date.today()
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        dedicated_team_quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_quarter.DedicatedTeamQuarter,
            related_field_names=["dedicated_team_id", "quarter_id"],
            foreign_field_names=["dedicated_team_id", "quarter_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_id", "planning_period_id"],
            foreign_field_names=["project_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter.ProjectTeamQuarter,
            related_field_names=["project_team_id", "quarter_id"],
            foreign_field_names=["project_team_id", "quarter_id"],
            pulled_field_name="id",
            default=-1
        )

        system_change_requests_analysis_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        system_change_requests_development_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        system_change_requests_testing_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="testing_estimate",
            aggregate_function="sum",
            default=0
        )

        system_change_requests_management_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="management_estimate",
            aggregate_function="sum",
            default=0
        )

        system_change_requests_estimate_sum = cubista.CalculatedField(
            lambda_expression=lambda x: x["system_change_requests_analysis_estimate_sum"] + x["system_change_requests_development_estimate_sum"] + x["system_change_requests_testing_estimate_sum"] + x["system_change_requests_management_estimate_sum"],
            source_fields=["system_change_requests_analysis_estimate_sum", "system_change_requests_development_estimate_sum", "system_change_requests_testing_estimate_sum", "system_change_requests_management_estimate_sum"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        management_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="management_time_spent",
            aggregate_function="sum",
            default=0
        )

        incident_fixing_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        non_project_activity_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["testing_time_spent"] + x["management_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "testing_time_spent", "management_time_spent"]
        )

        analysis_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["analysis_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["analysis_express_estimate"] if not pd.isnull(x["analysis_express_estimate"]) else 0,
                        x["system_change_requests_analysis_estimate_sum"],
                        x["analysis_time_spent"]
                    )
                ),
            source_fields=["analysis_time_spent", "state_category_id", "analysis_express_estimate", "system_change_requests_analysis_estimate_sum"]
        )

        development_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["development_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["development_express_estimate"] if not pd.isnull(x["development_express_estimate"]) else 0,
                        x["system_change_requests_development_estimate_sum"],
                        x["development_time_spent"]
                    )
                ),
            source_fields=["development_time_spent", "state_category_id", "development_express_estimate", "system_change_requests_development_estimate_sum"]
        )

        testing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["testing_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["testing_express_estimate"] if not pd.isnull(x["testing_express_estimate"]) else 0,
                        x["system_change_requests_testing_estimate_sum"],
                        x["testing_time_spent"]
                    )
                ),
            source_fields=["testing_time_spent", "state_category_id", "testing_express_estimate", "system_change_requests_testing_estimate_sum"]
        )

        management_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["management_time_spent"],
            source_fields=["management_time_spent"]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_estimate"] + x["development_estimate"] + x["testing_estimate"] + x["management_estimate"],
            source_fields=["analysis_estimate", "development_estimate", "testing_estimate", "management_estimate"]
        )

        time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] - x["time_spent"],
            source_fields=["estimate", "time_spent"]
        )

        analysis_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["analysis_estimate"] - x["analysis_time_spent"],
            source_fields=["analysis_estimate", "analysis_time_spent"]
        )

        development_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["development_estimate"] - x["development_time_spent"],
            source_fields=["development_estimate", "development_time_spent"]
        )

        testing_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["testing_estimate"] - x["testing_time_spent"],
            source_fields=["testing_estimate", "testing_time_spent"]
        )

        child_function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or x["key"] in ChangeRequest.CHANGE_REQUESTS_WITHOUT_FUNCTION_POINTS else x["child_function_points"],
            source_fields=["is_cancelled", "child_function_points", "key"]
        )

        child_function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or x["key"] in ChangeRequest.CHANGE_REQUESTS_WITHOUT_FUNCTION_POINTS else x["child_function_points_effort"],
            source_fields=["is_cancelled", "child_function_points_effort", "key"]
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["last_timesheet_date"] if x["time_left"] == 0 else (
                x["planning_period_end"] if x["time_sheets_by_date_model_m"] == 0 else (
                    x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"])
                )),
            source_fields=["last_timesheet_date", "time_left", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "planning_period_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        planned_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["install_date"] if not pd.isnull(x["install_date"]) else (
                x["resolution_date"] if not pd.isnull(x["resolution_date"]) and x["state_category_id"] == state.StateCategory.DONE else (
                    x["planned_install_date"] if not pd.isnull(x["planned_install_date"]) else (
                        x["quarter_end"] if x["quarter_id"] != -1 else (
                            datetime.date(year=x["year_label_max"], month=12, day=31) if x["year_label_max"] != -1 else None
                        )
                    )
                )
            ),
            source_fields=["install_date", "resolution_date", "state_category_id", "planned_install_date", "quarter_end", "year_label_max", "quarter_id"]
        )

        planned_install_date_delay_days = cubista.CalculatedField(
            lambda_expression=lambda x: (x["calculated_finish_date"] - x["planned_install_date"]).days if pd.notnull(x["calculated_finish_date"]) and pd.notnull(x["planned_install_date"]) else 0,
            source_fields=["calculated_finish_date", "planned_install_date"]
        )

        quarter_end_delay_days = cubista.CalculatedField(
            lambda_expression=lambda x: (x["calculated_finish_date"] - x["quarter_end"]).days if pd.notnull(x["calculated_finish_date"]) and pd.notnull(x["quarter_end"]) else 0,
            source_fields=["calculated_finish_date", "quarter_end"]
        )

        planning_period_end_delay_days = cubista.CalculatedField(
            lambda_expression=lambda x: (x["calculated_finish_date"] - x["planning_period_end"]).days if pd.notnull(x["calculated_finish_date"]) and pd.notnull(x["planning_period_end"]) else 0,
            source_fields=["calculated_finish_date", "planning_period_end"]
        )

        delay_days = cubista.CalculatedField(
            lambda_expression=lambda x: max(x["planned_install_date_delay_days"], x["quarter_end_delay_days"], x["planning_period_end_delay_days"]),
            source_fields=["planned_install_date_delay_days", "quarter_end_delay_days", "planning_period_end_delay_days"]
        )

        time_spent_in_current_quarter = cubista.PullByRelatedField(
            foreign_table=lambda: ChangeRequestTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_spent_in_current_quarter",
            default=0
        )

        time_spent_not_in_current_quarter = cubista.PullByRelatedField(
            foreign_table=lambda: ChangeRequestTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_spent_not_in_current_quarter",
            default=0
        )

        time_spent_chronon = cubista.PullByRelatedField(
            foreign_table=lambda: ChangeRequestTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_spent_chronon",
            default=0
        )

        last_timesheet_date = cubista.PullMaxByRelatedField(
            foreign_table=lambda: time_sheet.ChangeRequestTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["change_request_id"],
            max_field_name="time_spent_cumsum",
            pulled_field_name="date",
            default=datetime.date.today()
        )

class ChangeRequestTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestTimeSpent
        sort_by: [str] = []
        group_by: [str] = ["change_request_id", "project_team_id", "dedicated_team_id", "company_id", "planning_period_id", "quarter_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        quarter_id = cubista.AggregatedTableGroupField(source="quarter_id")
        time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")
        time_spent_not_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_not_in_current_quarter", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]
