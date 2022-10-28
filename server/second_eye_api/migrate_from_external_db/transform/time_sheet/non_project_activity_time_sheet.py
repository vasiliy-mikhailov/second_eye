import cubista
import datetime

from . import field_pack
from .. import non_project_activity
from .. import person
from .. import time_sheet
from .. import utils

class NonProjectActivityTimeSheet(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        non_project_activity_id = cubista.ForeignKeyField(foreign_table=lambda: non_project_activity.NonProjectActivity, default=-1, nulls=False)
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["non_project_activity_id"],
            source_fields=["non_project_activity_id"]
        )
        work_item_type = cubista.CalculatedField(
            lambda_expression=lambda x: time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_NON_PROJECT_ACTIVITY_TIME_SHEET,
            source_fields=[]
        )
        date = cubista.DateField(nulls=False)
        ordinal_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["date"].toordinal(),
            source_fields=["date"]
        )

        person_key = cubista.StringField()
        person_id = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_key"],
            foreign_field_names=["key"],
            pulled_field_name="id",
            default=-1
        )

        system_change_request_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        change_request_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        incident_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        project_team_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        project_manager_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        dedicated_team_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        epic_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: non_project_activity.NonProjectActivity, related_field_name="non_project_activity_id", pulled_field_name="company_id")

        has_value = cubista.CalculatedField(
            lambda_expression=lambda x: False,
            source_fields=[]
        )
        is_reengineering = cubista.CalculatedField(
            lambda_expression=lambda x: False,
            source_fields=[]
        )

        system_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        quarter_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
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

        non_project_activity_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
        )

        time_spent = cubista.FloatField(nulls=False)

        dedicated_team_planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        dedicated_team_quarter_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        project_team_planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        project_team_quarter_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )

        time_spent_with_value = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        time_spent_without_value = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"],
           source_fields=["time_spent"]
        )

        time_spent_for_reengineering = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        time_spent_not_for_reengineering = \
            cubista.CalculatedField(lambda_expression=lambda x: x["time_spent"],
           source_fields=["time_spent"]
        )

        is_outsource = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_id"],
            foreign_field_names=["id"],
            pulled_field_name="is_outsource",
            default=False
        )

        time_spent_in_current_quarter = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if utils.is_in_current_quarter(for_date=x["date"]) else 0,
            source_fields=["date", "time_spent"]
        )

        time_spent_not_in_current_quarter = cubista.CalculatedField(lambda_expression=lambda x:
            0 if utils.is_in_current_quarter(for_date=x["date"]) else x["time_spent"],
            source_fields=["date", "time_spent"]
        )

        time_spent_in_25_to_5_working_days_back_window = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"] if utils.is_in_chronon_bounds(for_date=x["date"], sys_date=datetime.date.today()) else 0,
            source_fields=["date", "time_spent"]
        )

        time_spent_in_25_to_5_working_days_back_window_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent_in_25_to_5_working_days_back_window"] / 160,
            source_fields=["time_spent_in_25_to_5_working_days_back_window"]
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPack(),
            lambda: field_pack.ChrononFieldPackForNormalTable(),
        ]