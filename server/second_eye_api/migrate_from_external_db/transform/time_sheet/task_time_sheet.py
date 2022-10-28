import cubista
import datetime

from .. import dedicated_team_planning_period
from .. import dedicated_team_planning_period_system
from .. import dedicated_team_quarter
from .. import dedicated_team_quarter_system
from .. import field_pack
from .. import person
from .. import project_team_planning_period
from .. import project_team_planning_period_system
from .. import project_team_quarter
from .. import project_team_quarter_system
from .. import skill
from .. import system_planning_period
from .. import task
from .. import time_sheet
from .. import utils

class TaskTimeSheet(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        task_id = cubista.ForeignKeyField(foreign_table=lambda: task.Task, default=-1, nulls=False)
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["task_id"],
            source_fields=["task_id"]
        )
        work_item_type = cubista.CalculatedField(
            lambda_expression=lambda x: time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_TASK_TIME_SHEET,
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

        system_change_request_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="system_change_request_id")
        change_request_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="change_request_id")
        incident_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        non_project_activity_id = cubista.CalculatedField(
            lambda_expression=lambda x: -1,
            source_fields=[]
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="project_team_id")
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="project_manager_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="dedicated_team_id")
        epic_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="epic_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="company_id")
        has_value = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="has_value")
        is_reengineering = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="is_reengineering")
        system_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="system_id")
        planning_period_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="planning_period_id")
        quarter_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="quarter_id")
        skill_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: task.Task, related_field_name="task_id", pulled_field_name="skill_id")

        analysis_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["skill_id"] == skill.Skill.ANALYSIS else 0,
            source_fields=["time_spent", "skill_id"]
        )

        development_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["skill_id"] == skill.Skill.DEVELOPMENT else 0,
            source_fields=["time_spent", "skill_id"]
        )

        testing_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["skill_id"] == skill.Skill.TESTING else 0,
            source_fields=["time_spent", "skill_id"]
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

        project_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period_system.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_id", "planning_period_id", "system_id"],
            foreign_field_names=["project_team_id", "planning_period_id", "system_id"],
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

        dedicated_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period_system.DedicatedTeamPlanningPeriodSystem,
            related_field_names=["dedicated_team_id", "planning_period_id", "system_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id", "system_id"],
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

        system_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: system_planning_period.SystemPlanningPeriod,
            related_field_names=["system_id", "planning_period_id"],
            foreign_field_names=["system_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

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


class TaskTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: TaskTimeSheet
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = [
            "task_id", "system_change_request_id", "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "system_id", "epic_id", "planning_period_id",
            "project_team_planning_period_id", "project_team_quarter_id", "dedicated_team_planning_period_id", "dedicated_team_quarter_id",
            "project_team_planning_period_system_id", "project_team_quarter_system_id", "dedicated_team_planning_period_system_id", "dedicated_team_quarter_system_id",
            "system_planning_period_id",
            "ordinal_date", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        task_id = cubista.AggregatedTableGroupField(source="task_id")
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        project_team_planning_period_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_id")
        project_team_quarter_id = cubista.AggregatedTableGroupField(source="project_team_quarter_id")
        dedicated_team_planning_period_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_id")
        dedicated_team_quarter_id = cubista.AggregatedTableGroupField(source="dedicated_team_quarter_id")
        project_team_planning_period_system_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_system_id")
        project_team_quarter_system_id = cubista.AggregatedTableGroupField(source="project_team_quarter_system_id")
        dedicated_team_planning_period_system_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_system_id")
        dedicated_team_quarter_system_id = cubista.AggregatedTableGroupField(source="dedicated_team_quarter_system_id")
        system_planning_period_id = cubista.AggregatedTableGroupField(source="system_planning_period_id")

        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")

        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["task_id"], sort_by=["ordinal_date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_for_reengineering", aggregate_function="sum")
        time_spent_not_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_not_for_reengineering", aggregate_function="sum")
        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )
        month = cubista.AggregatedTableGroupField(source="month")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]