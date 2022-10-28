import cubista
import datetime

from .. import field_pack
from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class SystemChangeRequestTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.TaskTimeSheetByDate
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = [
            "system_change_request_id", "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "system_id", "epic_id", "planning_period_id",
            "project_team_planning_period_id", "project_team_quarter_id", "dedicated_team_planning_period_id", "dedicated_team_quarter_id",
            "project_team_planning_period_system_id", "project_team_quarter_system_id",
            "dedicated_team_planning_period_system_id", "dedicated_team_quarter_system_id",
            "system_planning_period_id",
            "ordinal_date", "month"
        ]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        project_team_planning_period_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_id")
        project_team_quarter_id = cubista.AggregatedTableGroupField(source="project_team_quarter_id")
        dedicated_team_planning_period_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_id")
        dedicated_team_quarter_id = cubista.AggregatedTableGroupField(source="dedicated_team_quarter_id")
        project_team_planning_period_system_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_system_id")
        project_team_quarter_system_id = cubista.AggregatedTableGroupField(source="project_team_quarter_system_id")
        dedicated_team_planning_period_system_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_system_id")
        dedicated_team_quarter_system_id = cubista.AggregatedTableGroupField(source="dedicated_team_quarter_system_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")

        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )
        month = cubista.AggregatedTableGroupField(source="month")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["ordinal_date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_for_reengineering", aggregate_function="sum")
        time_spent_not_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_not_for_reengineering", aggregate_function="sum")

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: SystemChangeRequestTimeSheetByDateModel,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["system_change_request_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: utils.normalize(
                x=x["date"], min_x=x["time_sheets_by_date_model_min_date"],
                max_x=x["time_sheets_by_date_model_max_date"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

class SystemChangeRequestTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        entity_id_field_name = "system_change_request_id"

    class Fields:
        system_change_request_id = time_sheet_by_date_model.EntityIdField(source="system_change_request_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")

class SystemChangeRequestAnalysisTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = ["system_change_request_id", "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "system_id", "epic_id", "system_planning_period_id", "ordinal_date"]
        filter = lambda x: x["analysis_time_spent"] > 0
        filter_fields: [str] = ["analysis_time_spent"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )
        time_spent = cubista.AggregatedTableAggregateField(source="analysis_time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["ordinal_date"])

class SystemChangeRequestDevelopmentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = ["system_change_request_id", "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "system_id", "epic_id", "system_planning_period_id", "ordinal_date"]
        filter = lambda x: x["development_time_spent"] > 0
        filter_fields: [str] = ["development_time_spent"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")
        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )
        time_spent = cubista.AggregatedTableAggregateField(source="development_time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["ordinal_date"])

class SystemChangeRequestTestingTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = ["system_change_request_id", "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "system_id", "epic_id", "system_planning_period_id", "ordinal_date"]
        filter = lambda x: x["testing_time_spent"] > 0
        filter_fields: [str] = ["testing_time_spent"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")
        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )
        time_spent = cubista.AggregatedTableAggregateField(source="testing_time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["ordinal_date"])