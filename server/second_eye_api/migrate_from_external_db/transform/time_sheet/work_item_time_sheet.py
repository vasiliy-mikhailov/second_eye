import cubista
import datetime

from . import dedicated_team_planning_period
from . import dedicated_team_planning_period_system
from . import dedicated_team_quarter
from . import dedicated_team_quarter_system
from . import project_team_planning_period
from . import project_team_planning_period_system
from . import project_team_quarter
from . import project_team_quarter_system
from . import person
from . import system_planning_period
from . import time_sheet

"system_change_request_id", "change_request_id", "epic_id",
"dedicated_team_planning_period_system_id", "dedicated_team_quarter_system_id",
"system_planning_period_id"

class WorkItemTimeSheet(cubista.UnionTable):
    WORK_ITEM_TYPE_INCIDENT_NO_INCIDENT_SUB_TASK_AGGREGATION_TIME_SHEET = 1
    WORK_ITEM_TYPE_INCIDENT_SUB_TASK_TIME_SHEET = 2
    WORK_ITEM_TYPE_MANAGEMENT_TIME_SHEET = 3
    WORK_ITEM_TYPE_NON_PROJECT_ACTIVITY_TIME_SHEET = 4
    WORK_ITEM_TYPE_TASK_TIME_SHEET = 5

    class Union:
        tables: [cubista.Table] = [
            lambda: time_sheet.IncidentNoIncidentSubTaskAggregationTimeSheet,
            lambda: time_sheet.IncidentSubTaskTimeSheet,
            lambda: time_sheet.ManagementTimeSheet,
            lambda: time_sheet.NonProjectActivityTimeSheet,
            lambda: time_sheet.TaskTimeSheet,
        ]

        fields: [str] = [
            "work_item_id",
            "work_item_type",
            "date",
            "ordinal_date",
            "month",
            "analysis_time_spent",
            "analysis_time_spent_month_fte",
            "development_time_spent",
            "development_time_spent_month_fte",
            "testing_time_spent",
            "testing_time_spent_month_fte",
            "management_time_spent",
            "management_time_spent_month_fte",
            "incident_fixing_time_spent",
            "incident_fixing_time_spent_month_fte",
            "non_project_activity_time_spent",
            "non_project_activity_time_spent_month_fte",
            "time_spent",
            "time_spent_month_fte",
            "is_in_chronon",
            "analysis_time_spent_chronon",
            "development_time_spent_chronon",
            "testing_time_spent_chronon",
            "management_time_spent_chronon",
            "incident_fixing_time_spent_chronon",
            "non_project_activity_time_spent_chronon",
            "time_spent_chronon",
            "analysis_time_spent_chronon_fte",
            "development_time_spent_chronon_fte",
            "testing_time_spent_chronon_fte",
            "management_time_spent_chronon_fte",
            "incident_fixing_time_spent_chronon_fte",
            "non_project_activity_time_spent_chronon_fte",
            "time_spent_chronon_fte",
            "person_key",
            "person_id",
            "system_change_request_id",
            "change_request_id",
            "incident_id",
            "non_project_activity_id",
            "project_team_id",
            "project_manager_id",
            "dedicated_team_id",
            "epic_id",
            "company_id",
            "has_value",
            "is_reengineering",
            "system_id",
            "planning_period_id",
            "time_spent_with_value",
            "time_spent_without_value",
            "time_spent_for_reengineering",
            "time_spent_not_for_reengineering",
            "is_outsource",
            "time_spent_in_current_quarter",
            "time_spent_not_in_current_quarter",
            "time_spent_in_25_to_5_working_days_back_window",
            "time_spent_in_25_to_5_working_days_back_window_fte",
            "quarter_id",
        ]

    class Fields:
        id = cubista.UnionTableTableAutoIncrementPrimaryKeyField()
        work_item_id = cubista.UnionTableUnionField(source="work_item_id")
        work_item_type = cubista.UnionTableUnionField(source="work_item_type")
        date = cubista.UnionTableUnionField(source="date")
        month = cubista.UnionTableUnionField(source="month")
        ordinal_date = cubista.UnionTableUnionField(source="ordinal_date")
        analysis_time_spent = cubista.UnionTableUnionField(source="analysis_time_spent")
        analysis_time_spent_month_fte = cubista.UnionTableUnionField(source="analysis_time_spent_month_fte")
        development_time_spent = cubista.UnionTableUnionField(source="development_time_spent")
        development_time_spent_month_fte = cubista.UnionTableUnionField(source="development_time_spent_month_fte")
        testing_time_spent = cubista.UnionTableUnionField(source="testing_time_spent")
        testing_time_spent_month_fte = cubista.UnionTableUnionField(source="testing_time_spent_month_fte")
        management_time_spent = cubista.UnionTableUnionField(source="management_time_spent")
        management_time_spent_month_fte = cubista.UnionTableUnionField(source="management_time_spent_month_fte")
        incident_fixing_time_spent = cubista.UnionTableUnionField(source="incident_fixing_time_spent")
        incident_fixing_time_spent_month_fte = cubista.UnionTableUnionField(source="incident_fixing_time_spent_month_fte")
        non_project_activity_time_spent = cubista.UnionTableUnionField(source="non_project_activity_time_spent")
        non_project_activity_time_spent_month_fte = cubista.UnionTableUnionField(source="non_project_activity_time_spent_month_fte")

        time_spent = cubista.UnionTableUnionField(source="time_spent")
        time_spent_month_fte = cubista.UnionTableUnionField(source="time_spent_month_fte")

        is_in_chronon = cubista.UnionTableUnionField(source="is_in_chronon")
        analysis_time_spent_chronon = cubista.UnionTableUnionField(source="analysis_time_spent_chronon")
        development_time_spent_chronon = cubista.UnionTableUnionField(source="development_time_spent_chronon")
        testing_time_spent_chronon = cubista.UnionTableUnionField(source="testing_time_spent_chronon")
        management_time_spent_chronon = cubista.UnionTableUnionField(source="management_time_spent_chronon")
        incident_fixing_time_spent_chronon = cubista.UnionTableUnionField(source="incident_fixing_time_spent_chronon")
        non_project_activity_time_spent_chronon = cubista.UnionTableUnionField(source="non_project_activity_time_spent_chronon")
        time_spent_chronon = cubista.UnionTableUnionField(source="time_spent_chronon")
        analysis_time_spent_chronon_fte = cubista.UnionTableUnionField(source="analysis_time_spent_chronon_fte")
        development_time_spent_chronon_fte = cubista.UnionTableUnionField(source="development_time_spent_chronon_fte")
        testing_time_spent_chronon_fte = cubista.UnionTableUnionField(source="testing_time_spent_chronon_fte")
        management_time_spent_chronon_fte = cubista.UnionTableUnionField(source="management_time_spent_chronon_fte")
        incident_fixing_time_spent_chronon_fte = cubista.UnionTableUnionField(source="incident_fixing_time_spent_chronon_fte")
        non_project_activity_time_spent_chronon_fte = cubista.UnionTableUnionField(source="non_project_activity_time_spent_chronon_fte")
        time_spent_chronon_fte = cubista.UnionTableUnionField(source="time_spent_chronon_fte")

        person_key = cubista.UnionTableUnionField(source="person_key")
        person_id = cubista.UnionTableUnionField(source="person_id")
        system_change_request_id = cubista.UnionTableUnionField(source="system_change_request_id")
        change_request_id = cubista.UnionTableUnionField(source="change_request_id")
        incident_id = cubista.UnionTableUnionField(source="incident_id")
        non_project_activity_id = cubista.UnionTableUnionField(source="non_project_activity_id")
        project_team_id = cubista.UnionTableUnionField(source="project_team_id")
        project_manager_id = cubista.UnionTableUnionField(source="project_manager_id")
        dedicated_team_id = cubista.UnionTableUnionField(source="dedicated_team_id")
        epic_id = cubista.UnionTableUnionField(source="epic_id")
        company_id = cubista.UnionTableUnionField(source="company_id")
        has_value = cubista.UnionTableUnionField(source="has_value")
        is_reengineering = cubista.UnionTableUnionField(source="is_reengineering")
        system_id = cubista.UnionTableUnionField(source="system_id")
        planning_period_id = cubista.UnionTableUnionField(source="planning_period_id")
        time_spent_with_value = cubista.UnionTableUnionField(source="time_spent_with_value")
        time_spent_without_value = cubista.UnionTableUnionField(source="time_spent_without_value")
        time_spent_for_reengineering = cubista.UnionTableUnionField(source="time_spent_for_reengineering")
        time_spent_not_for_reengineering = cubista.UnionTableUnionField(source="time_spent_not_for_reengineering")
        is_outsource = cubista.UnionTableUnionField(source="is_outsource")
        time_spent_in_current_quarter = cubista.UnionTableUnionField(source="time_spent_in_current_quarter")
        time_spent_not_in_current_quarter = cubista.UnionTableUnionField(source="time_spent_not_in_current_quarter")
        time_spent_in_25_to_5_working_days_back_window = cubista.UnionTableUnionField(source="time_spent_in_25_to_5_working_days_back_window")
        time_spent_in_25_to_5_working_days_back_window_fte = cubista.UnionTableUnionField(source="time_spent_in_25_to_5_working_days_back_window_fte")
        quarter_id = cubista.UnionTableUnionField(source="quarter_id")

        days_between_this_time_sheet_and_persons_last_time_sheet = cubista.CalculatedField(
            lambda_expression=lambda x: (x["person_last_timesheet_date"] - x["date"]).days,
            source_fields=["person_last_timesheet_date", "date"]
        )

        person_last_timesheet_date = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_id"],
            foreign_field_names=["id"],
            pulled_field_name="last_timesheet_date",
            default=datetime.date.today()
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        dedicated_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period_system.DedicatedTeamPlanningPeriodSystem,
            related_field_names=["dedicated_team_id", "planning_period_id", "system_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id", "system_id"],
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

        project_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period_system.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_id", "planning_period_id", "system_id"],
            foreign_field_names=["project_team_id", "planning_period_id", "system_id"],
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

        dedicated_team_quarter_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_quarter_system.DedicatedTeamQuarterSystem,
            related_field_names=["dedicated_team_id", "quarter_id", "system_id"],
            foreign_field_names=["dedicated_team_id", "quarter_id", "system_id"],
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

        project_team_quarter_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter_system.ProjectTeamQuarterSystem,
            related_field_names=["project_team_id", "quarter_id", "system_id"],
            foreign_field_names=["project_team_id", "quarter_id", "system_id"],
            pulled_field_name="id",
            default=-1
        )

        system_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: system_planning_period.SystemPlanningPeriod,
            related_field_names=["system_id", "planning_period_id"],
            foreign_field_names=["system_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

