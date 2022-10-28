import cubista
import datetime

from .. import field_pack
from .. import project_team
from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class ProjectTeamTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestTimeSheetByDate
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = [
            "project_team_id", "dedicated_team_id", "company_id",
            "ordinal_date"
        ]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )

        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["project_team_id"], sort_by=["date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_with_value_cumsum = cubista.CumSumField(source_field="time_spent_with_value", group_by=["project_team_id"], sort_by=["date"])
        time_spent_without_value_cumsum = cubista.CumSumField(source_field="time_spent_without_value", group_by=["project_team_id"], sort_by=["date"])

        time_spent_with_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_with_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_with_value_cumsum", "time_spent_cumsum"]
        )

        time_spent_without_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_without_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_without_value_cumsum", "time_spent_cumsum"]
        )

        time_spent_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_for_reengineering", aggregate_function="sum")
        time_spent_not_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_not_for_reengineering", aggregate_function="sum")
        time_spent_for_reengineering_cumsum = cubista.CumSumField(source_field="time_spent_for_reengineering", group_by=["project_team_id"], sort_by=["date"])
        time_spent_not_for_reengineering_cumsum = cubista.CumSumField(source_field="time_spent_not_for_reengineering", group_by=["project_team_id"], sort_by=["date"])

        time_spent_for_reengineering_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_for_reengineering_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_for_reengineering_cumsum", "time_spent_cumsum"]
        )

        time_spent_not_for_reengineering_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_not_for_reengineering_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_not_for_reengineering_cumsum", "time_spent_cumsum"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamTimeSheetByDateModel,
            related_field_names=["project_team_id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamTimeSheetByDateModel,
            related_field_names=["project_team_id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamTimeSheetByDateModel,
            related_field_names=["project_team_id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamTimeSheetByDateModel,
            related_field_names=["project_team_id"],
            foreign_field_names=["project_team_id"],
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
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

class ProjectTeamTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: ProjectTeamTimeSheetByDate
        entity_id_field_name = "project_team_id"

    class Fields:
        project_team_id = time_sheet_by_date_model.EntityIdField(source="project_team_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")

class ProjectTeamTimeSheetByMonth(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = ["month"]
        group_by: [str] = ["project_team_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        month = cubista.AggregatedTableGroupField(source="month")

        dedicated_team_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeam,
            related_field_names=["project_team_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_id",
            default=-1
        )

        working_days_in_month_occured = cubista.CalculatedField(
            lambda_expression=lambda x: utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()),
            source_fields=["month"]
        )

        analysis_time_spent_fte = cubista.AggregatedTableAggregateField(source="analysis_time_spent_month_fte", aggregate_function="sum")
        development_time_spent_fte = cubista.AggregatedTableAggregateField(source="development_time_spent_month_fte", aggregate_function="sum")
        testing_time_spent_fte = cubista.AggregatedTableAggregateField(source="testing_time_spent_month_fte", aggregate_function="sum")
        management_time_spent_fte = cubista.AggregatedTableAggregateField(source="management_time_spent_month_fte", aggregate_function="sum")
        incident_fixing_time_spent_fte = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent_month_fte", aggregate_function="sum")
        non_project_activity_time_spent_fte = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent_month_fte", aggregate_function="sum")
        time_spent_fte = cubista.AggregatedTableAggregateField(source="time_spent_month_fte", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

class ProjectTeamAnalysisTimeSheetByMonth(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestAnalysisTimeSheetByDate
        sort_by: [str] = ["month"]
        group_by: [str] = ["project_team_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        month = cubista.AggregatedTableGroupField(source="month")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

        time_spent_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"] / 8 / utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) if utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) else 0,
            source_fields=["time_spent", "month"]
        )

class ProjectTeamDevelopmentTimeSheetByMonth(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestDevelopmentTimeSheetByDate
        sort_by: [str] = ["month"]
        group_by: [str] = ["project_team_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        month = cubista.AggregatedTableGroupField(source="month")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

        time_spent_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"] / 8 / utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) if utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) else 0,
            source_fields=["time_spent", "month"]
        )

class ProjectTeamTestingTimeSheetByMonth(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestTestingTimeSheetByDate
        sort_by: [str] = ["month"]
        group_by: [str] = ["project_team_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        month = cubista.AggregatedTableGroupField(source="month")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

        time_spent_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"] / 8 / utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) if utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) else 0,
            source_fields=["time_spent", "month"]
        )

class ProjectTeamIncidentFixingTimeSheetByMonth(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.IncidentTimeSheet
        sort_by: [str] = ["month"]
        group_by: [str] = ["project_team_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        month = cubista.AggregatedTableGroupField(source="month")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

        time_spent_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"] / 8 / utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) if utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()) else 0,
            source_fields=["time_spent", "month"]
        )