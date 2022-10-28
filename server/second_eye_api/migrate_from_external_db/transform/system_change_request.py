import cubista
import datetime
import pandas as pd

from . import change_request
from . import dedicated_team_planning_period
from . import dedicated_team_planning_period_system
from . import dedicated_team_quarter_system
from . import epic_system
from . import field_pack
from . import person_system_change_request
from . import planning_period
from . import project_team
from . import project_team_planning_period
from . import project_team_planning_period_system
from . import project_team_quarter_system
from . import state
from . import system
from . import system_change_request
from . import system_planning_period
from . import task
from . import time_sheet

class SystemChangeRequest(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        system_id = cubista.ForeignKeyField(foreign_table=lambda: system.System, default=-1, nulls=False)
        system_has_function_points = cubista.PullByForeignPrimaryKeyField(lambda: system.System, related_field_name="system_id", pulled_field_name="has_function_points")
        analysis_preliminary_estimate = cubista.FloatField(nulls=True)
        development_preliminary_estimate = cubista.FloatField(nulls=True)
        testing_preliminary_estimate = cubista.FloatField(nulls=True)
        analysis_planned_estimate = cubista.FloatField(nulls=True)
        development_planned_estimate = cubista.FloatField(nulls=True)
        testing_planned_estimate = cubista.FloatField(nulls=True)
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default="-1", nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        change_request_id = cubista.ForeignKeyField(foreign_table=lambda: change_request.ChangeRequest, default=-1, nulls=False)
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="project_team_id")
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="project_manager_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="dedicated_team_id")
        epic_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="epic_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="company_id")
        change_request_is_cancelled = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="is_cancelled"
        )

        has_value = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="has_value")
        is_reengineering = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="is_reengineering")
        planning_period_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="planning_period_id")
        quarter_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="quarter_id")

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

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_id", "planning_period_id"],
            foreign_field_names=["project_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        system_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: system_planning_period.SystemPlanningPeriod,
            related_field_names=["system_id", "planning_period_id"],
            foreign_field_names=["system_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        epic_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: epic_system.EpicSystem,
            related_field_names=["epic_id", "system_id"],
            foreign_field_names=["epic_id", "system_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriodSystem,
            related_field_names=["system_id", "planning_period_id", "project_team_id"],
            foreign_field_names=["system_id", "planning_period_id", "project_team_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period_system.ProjectTeamPlanningPeriodSystem,
            related_field_names=["system_id", "planning_period_id", "project_team_id"],
            foreign_field_names=["system_id", "planning_period_id", "project_team_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_quarter_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter_system.ProjectTeamQuarterSystem,
            related_field_names=["system_id", "quarter_id", "project_team_id"],
            foreign_field_names=["system_id", "quarter_id", "project_team_id"],
            pulled_field_name="id",
            default=-1
        )

        dedicated_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period_system.DedicatedTeamPlanningPeriodSystem,
            related_field_names=["system_id", "planning_period_id", "dedicated_team_id"],
            foreign_field_names=["system_id", "planning_period_id", "dedicated_team_id"],
            pulled_field_name="id",
            default=-1
        )

        dedicated_team_quarter_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_quarter_system.DedicatedTeamQuarterSystem,
            related_field_names=["system_id", "quarter_id", "dedicated_team_id"],
            foreign_field_names=["system_id", "quarter_id", "dedicated_team_id"],
            pulled_field_name="id",
            default=-1
        )

        analysis_tasks_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        development_tasks_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        testing_tasks_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="testing_estimate",
            aggregate_function="sum",
            default=0
        )

        tasks_estimate_sum = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_tasks_estimate_sum"] + x["development_tasks_estimate_sum"] + x["testing_tasks_estimate_sum"],
            source_fields=["analysis_tasks_estimate_sum", "development_tasks_estimate_sum", "testing_tasks_estimate_sum"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        management_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: time_sheet.ManagementTimeSheet,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="time_spent",
            aggregate_function="sum",
            default=0
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["testing_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "testing_time_spent"]
        )

        analysis_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["analysis_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["analysis_planned_estimate"] if not pd.isnull(x["analysis_planned_estimate"]) else (
                            x["analysis_preliminary_estimate"] if not pd.isnull(x["analysis_preliminary_estimate"]) else 0
                        ),
                        x["analysis_tasks_estimate_sum"],
                        x["analysis_time_spent"]
                    )
                ),
            source_fields=["analysis_time_spent", "state_category_id", "analysis_planned_estimate", "analysis_preliminary_estimate", "analysis_tasks_estimate_sum"]
        )

        development_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["development_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["development_planned_estimate"] if not pd.isnull(x["development_planned_estimate"]) else (
                            x["development_preliminary_estimate"] if not pd.isnull(x["development_preliminary_estimate"]) else 0
                        ),
                        x["development_tasks_estimate_sum"],
                        x["development_time_spent"]
                    )
                ),
            source_fields=["development_time_spent", "state_category_id", "development_planned_estimate", "development_preliminary_estimate", "development_tasks_estimate_sum"]
        )

        testing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["testing_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["testing_planned_estimate"] if not pd.isnull(x["testing_planned_estimate"]) else (
                            x["testing_preliminary_estimate"] if not pd.isnull(x["testing_preliminary_estimate"]) else 0
                        ),
                        x["testing_tasks_estimate_sum"],
                        x["testing_time_spent"]
                    )
                ),
            source_fields=["testing_time_spent", "state_category_id", "testing_planned_estimate", "testing_preliminary_estimate", "testing_tasks_estimate_sum"]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_estimate"] + x["development_estimate"] + x["testing_estimate"],
            source_fields=["analysis_estimate", "development_estimate", "testing_estimate"]
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
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or x["change_request_is_cancelled"] or not x["system_has_function_points"] else x["child_function_points"],
            source_fields=["is_cancelled", "child_function_points", "system_has_function_points", "change_request_is_cancelled"]
        )

        function_points_effort = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or x["change_request_is_cancelled"] or not x["system_has_function_points"] else x["analysis_estimate"] + x["development_estimate"] + x["management_time_spent"],
            source_fields=["analysis_estimate", "development_estimate", "management_time_spent", "system_has_function_points", "is_cancelled", "change_request_is_cancelled"]
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if not x["system_has_function_points"] or x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points", "system_has_function_points"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["planning_period_end"] if x["time_sheets_by_date_model_m"] == 0 else
                x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"]),
            source_fields=["time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "planning_period_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        main_developer_id = cubista.PullMaxByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequestDeveloper,
            related_field_names=["id"],
            foreign_field_names=["system_change_request_id"],
            max_field_name="time_spent",
            pulled_field_name="person_id",
            default=-1
        )

class SystemChangeRequestTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["system_change_request_id", "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "planning_period_id", "quarter_id", "system_id"]
        filter = lambda x: x["work_item_type"] in [time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_MANAGEMENT_TIME_SHEET, time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_TASK_TIME_SHEET]
        filter_fields: [str] = ["work_item_type"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        quarter_id = cubista.AggregatedTableGroupField(source="quarter_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")
        time_spent_not_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_not_in_current_quarter", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]


class SystemChangeRequestDeveloper(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: person_system_change_request.PersonSystemChangeRequestTimeSpent
        sort_by: [str] = []
        group_by: [str] = ["system_change_request_id", "person_id"]
        filter = lambda x: x["development_time_spent"] > 0
        filter_fields: [str] = ["development_time_spent"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        person_id = cubista.AggregatedTableGroupField(source="person_id")