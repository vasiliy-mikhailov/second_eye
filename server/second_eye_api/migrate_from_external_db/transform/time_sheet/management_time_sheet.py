import cubista
import datetime

from .. import dedicated_team_planning_period
from .. import dedicated_team_quarter
from .. import field_pack
from .. import person
from .. import project_team_planning_period
from .. import project_team_quarter
from .. import system_change_request
from .. import utils
from .. import time_sheet

class ManagementTimeSheet(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        system_change_request_id = cubista.ForeignKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, default=-1, nulls=False)
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["system_change_request_id"],
            source_fields=["system_change_request_id"]
        )
        work_item_type = cubista.CalculatedField(
            lambda_expression=lambda x: time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_MANAGEMENT_TIME_SHEET,
            source_fields=[]
        )
        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="change_request_id"
        )
        incident_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        non_project_activity_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="planning_period_id"
        )

        quarter_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="quarter_id"
        )

        company_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="company_id"
        )
        epic_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="epic_id"
        )
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="dedicated_team_id"
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="project_team_id"
        )
        project_manager_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="project_manager_id"
        )
        system_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="system_id"
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

        analysis_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            0,
            source_fields=[]
        )

        development_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            0,
            source_fields=[]
        )

        testing_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            0,
            source_fields=[]
        )

        management_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"],
            source_fields=["time_spent"]
        )

        incident_fixing_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            0,
            source_fields=[]
        )

        non_project_activity_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        time_spent = cubista.FloatField(nulls=False)

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

        has_value = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="has_value")
        is_reengineering = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="is_reengineering")
        time_spent_with_value = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["has_value"] else 0,
            source_fields=["time_spent", "has_value"]
        )

        time_spent_without_value = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if not x["has_value"] else 0,
           source_fields=["time_spent", "has_value"]
        )

        time_spent_for_reengineering = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["is_reengineering"] else 0,
            source_fields=["time_spent", "is_reengineering"]
        )

        time_spent_not_for_reengineering = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if not x["is_reengineering"] else 0,
           source_fields=["time_spent", "is_reengineering"]
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

        time_spent_in_25_to_5_working_days_back_window = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if utils.is_in_chronon_bounds(for_date=x["date"], sys_date=datetime.date.today()) else 0,
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
