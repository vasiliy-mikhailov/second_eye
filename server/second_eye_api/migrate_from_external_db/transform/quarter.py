import datetime
import cubista

from . import change_request
from . import field_pack
from . import issue
from . import person_change_request
from . import time_sheet
from . import utils

class Quarter(cubista.Table):
    QUARTER_END_DAYS = {
        1: 31,
        2: 30,
        3: 30,
        4: 31,
    }

    QUARTER_ROMAN_NUMBERS = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV"
    }

    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.CalculatedField(
            lambda_expression=lambda x: "-1" if x["year"] == -1 else "{}-{}".format(
                x["year"],
                Quarter.QUARTER_ROMAN_NUMBERS[x["quarter_number"]]
            ),
            source_fields=["year", "quarter_number"]
        )
        name = cubista.StringField()
        planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["year"],
            source_fields=["year"]
        )
        year=cubista.IntField()
        quarter_number=cubista.IntField()

        start = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(year=x["year"], month=(x["quarter_number"] - 1) * 3 + 1, day=1)
                    if x["year"] != -1 and x["quarter_number"] != -1
                    else datetime.date.today(),
            source_fields=["year", "quarter_number"]
        )

        end = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(year=x["year"], month=x["quarter_number"] * 3, day=Quarter.QUARTER_END_DAYS[x["quarter_number"]])
                    if x["year"] != -1 and x["quarter_number"] != -1
                    else datetime.date.today(),
            source_fields=["year", "quarter_number"]
        )

        analysis_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="quarter_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        development_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="quarter_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        testing_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="quarter_id",
            aggregated_field_name="testing_estimate",
            aggregate_function="sum",
            default=0
        )

        management_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["management_time_spent"],
            source_fields=["management_time_spent"]
        )

        incident_fixing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_fixing_time_spent"],
            source_fields=["incident_fixing_time_spent"]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_estimate"] + x["development_estimate"] + x["testing_estimate"] + x["management_estimate"] + x["incident_fixing_estimate"],
            source_fields=["analysis_estimate", "development_estimate", "testing_estimate", "management_estimate", "incident_fixing_estimate"]
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

        function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="quarter_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="quarter_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.QuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["quarter_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.QuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["quarter_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.QuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["quarter_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.QuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["quarter_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["end"] if x["time_sheets_by_date_model_m"] < 1e-2 else
                x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"]),
            source_fields=["time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        change_request_calculated_date_after_quarter_end_issue_count = cubista.AggregatedForeignField(
            foreign_table=lambda: issue.ChangeRequestCalculatedDateAfterQuarterEndIssue,
            foreign_field_name="quarter_id",
            aggregated_field_name="id",
            aggregate_function="count",
            default=0
        )

        change_request_count = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="quarter_id",
            aggregated_field_name="id",
            aggregate_function="count",
            default=0
        )

        change_request_calculated_date_before_quarter_end_share = cubista.CalculatedField(
            lambda_expression=lambda x: 1 - x["change_request_calculated_date_after_quarter_end_issue_count"] / x["change_request_count"] if x["change_request_count"] else 1,
            source_fields=["change_request_calculated_date_after_quarter_end_issue_count", "change_request_count"]
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="quarter_id"
            ),
            lambda: field_pack.TimeSpentFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="quarter_id"
            ),
        ]

class ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: change_request.ChangeRequest
        sort_by: [str] = []
        group_by: [str] = ["id", "project_team_id", "project_team_quarter_id", "dedicated_team_id", "dedicated_team_quarter_id", "quarter_id"]
        filter = lambda x: x["quarter_id"] != utils.get_current_quarter_id() and x["time_spent_in_current_quarter"] > 0
        filter_fields: [str] = ["quarter_id", "time_spent_in_current_quarter"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="id", primary_key=False)
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id", primary_key=False)
        project_team_quarter_id = cubista.AggregatedTableGroupField(source="project_team_quarter_id", primary_key=False)
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id", primary_key=False)
        dedicated_team_quarter_id = cubista.AggregatedTableGroupField(source="dedicated_team_quarter_id", primary_key=False)
        quarter_id = cubista.AggregatedTableGroupField(source="quarter_id", primary_key=False)
        time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")

class PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "project_team_id"]
        filter = lambda x: x["quarter_id"] != utils.get_current_quarter_id() and x["time_spent_in_current_quarter"] > 0
        filter_fields: [str] = ["quarter_id", "time_spent_in_current_quarter"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id", primary_key=False)
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id", primary_key=False)
        new_functions_time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")

