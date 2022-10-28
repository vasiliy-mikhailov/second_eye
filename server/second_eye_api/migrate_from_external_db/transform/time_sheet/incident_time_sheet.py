import cubista
import datetime


from .. import dedicated_team_planning_period
from .. import dedicated_team_quarter
from .. import field_pack
from .. import incident
from .. import incident_sub_task
from .. import person
from .. import project_team_planning_period
from .. import project_team_quarter
from .. import time_sheet
from .. import utils

class IncidentNoIncidentSubTaskAggregationTimeSheet(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        incident_id = cubista.ForeignKeyField(foreign_table=lambda: incident.Incident, default=-1, nulls=False)
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_id"],
            source_fields=["incident_id"]
        )

        work_item_type = cubista.CalculatedField(
            lambda_expression=lambda x: time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_INCIDENT_NO_INCIDENT_SUB_TASK_AGGREGATION_TIME_SHEET,
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
        non_project_activity_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="project_team_id")
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="project_manager_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="dedicated_team_id")
        epic_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="company_id")
        has_value = cubista.CalculatedField(
            lambda_expression=lambda x: True,
            source_fields=[]
        )
        is_reengineering = cubista.CalculatedField(
            lambda_expression=lambda x: True,
            source_fields=[]
        )
        system_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="system_id")
        planning_period_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="planning_period_id")
        quarter_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="quarter_id")

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
            lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
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

        time_spent_with_value = cubista.CalculatedField(lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
        )

        time_spent_without_value = cubista.CalculatedField(lambda_expression=lambda x: 0,
           source_fields=["time_spent"]
        )

        time_spent_for_reengineering = cubista.CalculatedField(lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
        )

        time_spent_not_for_reengineering = cubista.CalculatedField(lambda_expression=lambda x: 0,
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

class IncidentSubTaskTimeSheet(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        incident_sub_task_id = cubista.ForeignKeyField(foreign_table=lambda: incident_sub_task.IncidentSubTask, default=-1, nulls=False)
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_sub_task_id"],
            source_fields=["incident_sub_task_id"]
        )
        work_item_type = cubista.CalculatedField(
            lambda_expression=lambda x: time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_INCIDENT_SUB_TASK_TIME_SHEET,
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
        incident_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident_sub_task.IncidentSubTask, related_field_name="incident_sub_task_id", pulled_field_name="incident_id")
        non_project_activity_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="project_team_id")
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="project_manager_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="dedicated_team_id")
        epic_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="company_id")
        has_value = cubista.CalculatedField(
            lambda_expression=lambda x: True,
            source_fields=[]
        )
        is_reengineering = cubista.CalculatedField(
            lambda_expression=lambda x: True,
            source_fields=[]
        )
        system_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="system_id")
        planning_period_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="planning_period_id")
        quarter_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="quarter_id")

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

        incident_fixing_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"],
            source_fields=["time_spent"]
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

        time_spent_with_value = cubista.CalculatedField(lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
        )

        time_spent_without_value = cubista.CalculatedField(lambda_expression=lambda x: 0,
           source_fields=["time_spent"]
        )

        time_spent_for_reengineering = cubista.CalculatedField(lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
        )

        time_spent_not_for_reengineering = cubista.CalculatedField(lambda_expression=lambda x: 0,
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

class IncidentTimeSheet(cubista.UnionTable):
    class Union:
        tables: [cubista.Table] = [lambda: time_sheet.IncidentNoIncidentSubTaskAggregationTimeSheet, lambda: time_sheet.IncidentSubTaskTimeSheet]
        fields: [str] = [
            "incident_id",
            "work_item_id",
            "date",
            "ordinal_date",
            "month",
            "analysis_time_spent",
            "analysis_time_spent_chronon",
            "analysis_time_spent_chronon_fte",
            "analysis_time_spent_month_fte",
            "development_time_spent",
            "development_time_spent_chronon",
            "development_time_spent_chronon_fte",
            "development_time_spent_month_fte",
            "testing_time_spent",
            "testing_time_spent_chronon",
            "testing_time_spent_chronon_fte",
            "testing_time_spent_month_fte",
            "management_time_spent",
            "management_time_spent_chronon",
            "management_time_spent_chronon_fte",
            "management_time_spent_month_fte",
            "incident_fixing_time_spent",
            "incident_fixing_time_spent_chronon",
            "incident_fixing_time_spent_chronon_fte",
            "incident_fixing_time_spent_month_fte",
            "non_project_activity_time_spent",
            "non_project_activity_time_spent_chronon",
            "non_project_activity_time_spent_chronon_fte",
            "non_project_activity_time_spent_month_fte",
            "time_spent",
            "time_spent_chronon",
            "time_spent_chronon_fte",
            "time_spent_month_fte",
            "person_key",
            "person_id",
            "system_change_request_id",
            "change_request_id",
            "project_team_id",
            "project_manager_id",
            "dedicated_team_id",
            "epic_id",
            "company_id",
            "has_value",
            "is_reengineering",
            "system_id",
            "planning_period_id",
            "dedicated_team_planning_period_id",
            "project_team_planning_period_id",
            "time_spent_with_value",
            "time_spent_without_value",
            "time_spent_for_reengineering",
            "time_spent_not_for_reengineering",
            "is_outsource",
            "time_spent_in_current_quarter",
            "time_spent_not_in_current_quarter",
            "time_spent_in_25_to_5_working_days_back_window",
            "time_spent_in_25_to_5_working_days_back_window_fte",
        ]

    class Fields:
        id = cubista.UnionTableTableAutoIncrementPrimaryKeyField()
        incident_id = cubista.UnionTableUnionField(source="incident_id")
        work_item_id = cubista.UnionTableUnionField(source="work_item_id")
        date = cubista.UnionTableUnionField(source="date")
        ordinal_date = cubista.UnionTableUnionField(source="ordinal_date")
        month = cubista.UnionTableUnionField(source="month")
        analysis_time_spent = cubista.UnionTableUnionField(source="analysis_time_spent")
        analysis_time_spent_chronon = cubista.UnionTableUnionField(source="analysis_time_spent_chronon")
        analysis_time_spent_chronon_fte = cubista.UnionTableUnionField(source="analysis_time_spent_chronon_fte")
        analysis_time_spent_month_fte = cubista.UnionTableUnionField(source="analysis_time_spent_month_fte")
        development_time_spent = cubista.UnionTableUnionField(source="development_time_spent")
        development_time_spent_chronon = cubista.UnionTableUnionField(source="development_time_spent_chronon")
        development_time_spent_chronon_fte = cubista.UnionTableUnionField(source="development_time_spent_chronon_fte")
        development_time_spent_month_fte = cubista.UnionTableUnionField(source="development_time_spent_month_fte")
        testing_time_spent = cubista.UnionTableUnionField(source="testing_time_spent")
        testing_time_spent_chronon = cubista.UnionTableUnionField(source="testing_time_spent_chronon")
        testing_time_spent_chronon_fte = cubista.UnionTableUnionField(source="testing_time_spent_chronon_fte")
        testing_time_spent_month_fte = cubista.UnionTableUnionField(source="testing_time_spent_month_fte")
        management_time_spent = cubista.UnionTableUnionField(source="management_time_spent")
        management_time_spent_chronon = cubista.UnionTableUnionField(source="management_time_spent_chronon")
        management_time_spent_chronon_fte = cubista.UnionTableUnionField(source="management_time_spent_chronon_fte")
        management_time_spent_month_fte = cubista.UnionTableUnionField(source="management_time_spent_month_fte")
        incident_fixing_time_spent = cubista.UnionTableUnionField(source="incident_fixing_time_spent")
        incident_fixing_time_spent_chronon = cubista.UnionTableUnionField(source="incident_fixing_time_spent_chronon")
        incident_fixing_time_spent_chronon_fte = cubista.UnionTableUnionField(source="incident_fixing_time_spent_chronon_fte")
        incident_fixing_time_spent_month_fte = cubista.UnionTableUnionField(source="incident_fixing_time_spent_month_fte")
        non_project_activity_time_spent = cubista.UnionTableUnionField(source="non_project_activity_time_spent")
        non_project_activity_time_spent_chronon = cubista.UnionTableUnionField(source="non_project_activity_time_spent_chronon")
        non_project_activity_time_spent_chronon_fte = cubista.UnionTableUnionField(source="non_project_activity_time_spent_chronon_fte")
        non_project_activity_time_spent_month_fte = cubista.UnionTableUnionField(source="non_project_activity_time_spent_month_fte")
        time_spent = cubista.UnionTableUnionField(source="time_spent")
        time_spent_chronon = cubista.UnionTableUnionField(source="time_spent_chronon")
        time_spent_chronon_fte = cubista.UnionTableUnionField(source="time_spent_chronon_fte")
        time_spent_month_fte = cubista.UnionTableUnionField(source="time_spent_month_fte")
        person_key = cubista.UnionTableUnionField(source="person_key")
        person_id = cubista.UnionTableUnionField(source="person_id")
        system_change_request_id = cubista.UnionTableUnionField(source="system_change_request_id")
        change_request_id = cubista.UnionTableUnionField(source="change_request_id")
        project_team_id = cubista.UnionTableUnionField(source="project_team_id")
        project_manager_id = cubista.UnionTableUnionField(source="project_manager_id")
        dedicated_team_id = cubista.UnionTableUnionField(source="dedicated_team_id")
        epic_id = cubista.UnionTableUnionField(source="epic_id")
        company_id = cubista.UnionTableUnionField(source="company_id")
        has_value = cubista.UnionTableUnionField(source="has_value")
        is_reengineering = cubista.UnionTableUnionField(source="is_reengineering")
        planning_period_id = cubista.UnionTableUnionField(source="planning_period_id")
        dedicated_team_planning_period_id = cubista.UnionTableUnionField(source="dedicated_team_planning_period_id")
        project_team_planning_period_id = cubista.UnionTableUnionField(source="project_team_planning_period_id")
        time_spent_with_value = cubista.UnionTableUnionField(source="time_spent_with_value")
        time_spent_without_value = cubista.UnionTableUnionField(source="time_spent_without_value")
        time_spent_for_reengineering = cubista.UnionTableUnionField(source="time_spent_for_reengineering")
        time_spent_not_for_reengineering = cubista.UnionTableUnionField(source="time_spent_not_for_reengineering")
        is_outsource = cubista.UnionTableUnionField(source="is_outsource")
        time_spent_in_current_quarter = cubista.UnionTableUnionField(source="time_spent_in_current_quarter")
        time_spent_not_in_current_quarter = cubista.UnionTableUnionField(source="time_spent_not_in_current_quarter")
        time_spent_in_25_to_5_working_days_back_window = cubista.UnionTableUnionField(source="time_spent_in_25_to_5_working_days_back_window")
        time_spent_in_25_to_5_working_days_back_window_fte = cubista.UnionTableUnionField(source="time_spent_in_25_to_5_working_days_back_window_fte")

class IncidentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.IncidentTimeSheet
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = [
            "incident_id", "project_team_id", "dedicated_team_id", "company_id", "planning_period_id",
            "project_team_planning_period_id", "dedicated_team_planning_period_id",
            "ordinal_date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        incident_id = cubista.AggregatedTableGroupField(source="incident_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        project_team_planning_period_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_id")
        dedicated_team_planning_period_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_id")

        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")

        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["incident_id"], sort_by=["ordinal_date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_for_reengineering", aggregate_function="sum")
        time_spent_not_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_not_for_reengineering", aggregate_function="sum")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]