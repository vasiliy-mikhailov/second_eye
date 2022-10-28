import cubista

from . import company
from . import time_sheet

class NonProjectActivity(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        company_id = cubista.ForeignKeyField(foreign_table=lambda: company.Company, default=-1, nulls=False)
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["id"],
            source_fields=["id"]
        )

        non_project_activity_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: time_sheet.NonProjectActivityTimeSheet,
            foreign_field_name="non_project_activity_id",
            aggregated_field_name="time_spent",
            aggregate_function="sum",
            default=0
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["non_project_activity_time_spent"],
            source_fields=["non_project_activity_time_spent"]
        )

        planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        project_team_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        analysis_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        development_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        testing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
        )

        analysis_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        development_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        testing_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        management_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        incident_fixing_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        time_left = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        function_points_effort = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        quarter_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )