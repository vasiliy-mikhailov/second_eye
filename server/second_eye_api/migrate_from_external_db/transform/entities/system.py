import cubista
from . import planning_period
from . import system_change_request
import datetime
from .. import planning_period_time_sheet_by_date_model
from ..utils import normalize

class System(cubista.Table):
    SYSTEMS_WITHOUT_FUNCTION_POINTS = [
        "ACCL",
        "CREDIT",
        "CreditFrontOffice (MCB-CFO)",
        "DEPO",
        "Quorum",
        "Анализ вне системы",
        "Доступ в сеть МКБ",
        "Не указано",
        "Сквозная аналитика",
        "Тестирование стандартов, политик безопасности",
        "ЦФТ.ВХД",
        "ЦФТ.Депозиты",
    ]
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()
        has_function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["name"] in System.SYSTEMS_WITHOUT_FUNCTION_POINTS else 1,
            source_fields=["name"]
        )

        function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="system_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="system_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

class SystemPlanningPeriod(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequest
        sort_by: [str] = []
        group_by: [str] = ["planning_period_id", "system_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id", primary_key=False)
        system_id = cubista.AggregatedTableGroupField(source="system_id", primary_key=False)
        analysis_estimate = cubista.AggregatedTableAggregateField(source="analysis_estimate", aggregate_function="sum")
        development_estimate = cubista.AggregatedTableAggregateField(source="development_estimate", aggregate_function="sum")
        testing_estimate = cubista.AggregatedTableAggregateField(source="testing_estimate", aggregate_function="sum")
        estimate = cubista.AggregatedTableAggregateField(source="estimate", aggregate_function="sum")

        management_time_spent = cubista.AggregatedTableAggregateField(source="management_time_spent", aggregate_function="sum")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_left = cubista.AggregatedTableAggregateField(source="time_left", aggregate_function="sum")

        function_points = cubista.AggregatedTableAggregateField(source="function_points", aggregate_function="sum")
        function_points_effort = cubista.AggregatedTableAggregateField(source="function_points_effort", aggregate_function="sum")
        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        planning_period_start = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="start"
        )

        planning_period_end = planning_period.cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="end"
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_at_end_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: 1 * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        analysis_time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        analysis_time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        analysis_time_spent_cumsum_at_end_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: 1 * x["analysis_time_sheets_by_date_model_m"] + x["analysis_time_sheets_by_date_model_b"],
            source_fields=["analysis_time_sheets_by_date_model_m", "analysis_time_sheets_by_date_model_b"]
        )

        development_time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        development_time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        development_time_spent_cumsum_at_end_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: 1 * x["development_time_sheets_by_date_model_m"] + x["development_time_sheets_by_date_model_b"],
            source_fields=["development_time_sheets_by_date_model_m", "development_time_sheets_by_date_model_b"]
        )

        testing_time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        testing_time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        testing_time_spent_cumsum_at_end_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: 1 * x["testing_time_sheets_by_date_model_m"] + x["testing_time_sheets_by_date_model_b"],
            source_fields=["testing_time_sheets_by_date_model_m", "testing_time_sheets_by_date_model_b"]
        )

class SystemPlanningPeriodTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_id", "system_planning_period_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        system_id = cubista.AggregatedTableGroupField(source="system_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")
        date = cubista.AggregatedTableGroupField(source="date")


        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_planning_period_id"], sort_by=["date"])

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriod,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: normalize(
                x=x["date"], min_x=x["planning_period_start"],
                max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "planning_period_start", "planning_period_end", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class SystemPlanningPeriodTimeSheetByDateModel(planning_period_time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: SystemPlanningPeriodTimeSheetByDate
        planning_period_id_field_name = "system_planning_period_id"

    class Fields:
        system_planning_period_id = planning_period_time_sheet_by_date_model.PeriodIdField(source="system_planning_period_id")
        time_sheets_by_date_model_m = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")

class SystemPlanningPeriodAnalysisTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestAnalysisTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_id", "system_planning_period_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        system_id = cubista.AggregatedTableGroupField(source="system_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")
        date = cubista.AggregatedTableGroupField(source="date")


        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_planning_period_id"], sort_by=["date"])

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriod,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: normalize(
                x=x["date"], min_x=x["planning_period_start"],
                max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "planning_period_start", "planning_period_end", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class SystemPlanningPeriodAnalysisTimeSheetByDateModel(planning_period_time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: SystemPlanningPeriodAnalysisTimeSheetByDate
        planning_period_id_field_name = "system_planning_period_id"

    class Fields:
        system_planning_period_id = planning_period_time_sheet_by_date_model.PeriodIdField(source="system_planning_period_id")
        time_sheets_by_date_model_m = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")

class SystemPlanningPeriodDevelopmentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestDevelopmentTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_id", "system_planning_period_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        system_id = cubista.AggregatedTableGroupField(source="system_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_planning_period_id"], sort_by=["date"])

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriod,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: normalize(
                x=x["date"], min_x=x["planning_period_start"],
                max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "planning_period_start", "planning_period_end", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class SystemPlanningPeriodDevelopmentTimeSheetByDateModel(planning_period_time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: SystemPlanningPeriodDevelopmentTimeSheetByDate
        planning_period_id_field_name = "system_planning_period_id"

    class Fields:
        system_planning_period_id = planning_period_time_sheet_by_date_model.PeriodIdField(source="system_planning_period_id")
        time_sheets_by_date_model_m = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")

class SystemPlanningPeriodTestingTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestTestingTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_id", "system_planning_period_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        system_id = cubista.AggregatedTableGroupField(source="system_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")
        date = cubista.AggregatedTableGroupField(source="date")


        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_planning_period_id"], sort_by=["date"])

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriod,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["system_planning_period_id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: normalize(
                x=x["date"], min_x=x["planning_period_start"],
                max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "planning_period_start", "planning_period_end", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class SystemPlanningPeriodTestingTimeSheetByDateModel(planning_period_time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: SystemPlanningPeriodTestingTimeSheetByDate
        planning_period_id_field_name = "system_planning_period_id"

    class Fields:
        system_planning_period_id = planning_period_time_sheet_by_date_model.PeriodIdField(source="system_planning_period_id")
        time_sheets_by_date_model_m = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")