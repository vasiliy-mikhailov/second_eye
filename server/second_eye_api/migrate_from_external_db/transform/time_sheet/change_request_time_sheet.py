import cubista
import datetime

from .. import change_request
from .. import field_pack
from .. import planning_period
from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class ChangeRequestTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = [
            "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "epic_id", "planning_period_id",
            "project_team_planning_period_id", "project_team_quarter_id", "dedicated_team_planning_period_id", "dedicated_team_quarter_id",
            "ordinal_date", "month"
        ]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        project_team_planning_period_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_id")
        project_team_quarter_id = cubista.AggregatedTableGroupField(source="project_team_quarter_id")
        dedicated_team_planning_period_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_id")
        dedicated_team_quarter_id = cubista.AggregatedTableGroupField(source="dedicated_team_quarter_id")
        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )
        month = cubista.AggregatedTableGroupField(source="month")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_for_reengineering", aggregate_function="sum")
        time_spent_not_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_not_for_reengineering", aggregate_function="sum")

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

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ChangeRequestTimeSheetByDateModel,
            related_field_names=["change_request_id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ChangeRequestTimeSheetByDateModel,
            related_field_names=["change_request_id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: ChangeRequestTimeSheetByDateModel,
            related_field_names=["change_request_id"],
            foreign_field_names=["change_request_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: ChangeRequestTimeSheetByDateModel,
            related_field_names=["change_request_id"],
            foreign_field_names=["change_request_id"],
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

class ChangeRequestTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: ChangeRequestTimeSheetByDate
        entity_id_field_name = "change_request_id"

    class Fields:
        change_request_id = time_sheet_by_date_model.EntityIdField(source="change_request_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")


class ChangeRequestAnalysisTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestAnalysisTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        month = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date(x["date"].year, x["date"].month, 1),
            source_fields=["date"]
        )
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        epic_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="epic_id"
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_id"
        )


class ChangeRequestDevelopmentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestDevelopmentTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        month = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date(x["date"].year, x["date"].month, 1),
            source_fields=["date"]
        )
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        epic_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="epic_id"
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_id"
        )


class ChangeRequestTestingTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTestingTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        month = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date(x["date"].year, x["date"].month, 1),
            source_fields=["date"]
        )
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        epic_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="epic_id"
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_id"
        )