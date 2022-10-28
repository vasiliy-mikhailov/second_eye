import cubista

from . import field_pack
from . import system_change_request

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

        estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="system_id",
            aggregated_field_name="estimate",
            aggregate_function="sum",
            default=0
        )

        time_left = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="system_id",
            aggregated_field_name="time_left",
            aggregate_function="sum",
            default=0
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

class SystemTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestTimeSpent
        sort_by: [str] = []
        group_by: [str] = ["system_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")
        time_spent_not_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_not_in_current_quarter", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

