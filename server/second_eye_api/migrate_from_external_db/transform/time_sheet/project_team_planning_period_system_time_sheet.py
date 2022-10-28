import cubista
import datetime

from .. import planning_period
from .. import project_team_planning_period_system
from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class ProjectTeamPlanningPeriodSystemTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["project_team_planning_period_system_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_planning_period_system_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_system_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["project_team_planning_period_system_id"], sort_by=["date"])

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period_system.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_planning_period_id",
            default=-1
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period_system.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="project_team_planning_period_id",
            default=-1
        )

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period_system.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.date.today()
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.date.today()
        )

        dedicated_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period_system.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_planning_period_system_id",
            default=-1
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: utils.normalize(
                x=x["date"], min_x=x["time_sheets_by_date_model_min_date"],
                max_x=x["time_sheets_by_date_model_max_date"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class ProjectTeamPlanningPeriodSystemTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDate
        entity_id_field_name = "project_team_planning_period_system_id"

    class Fields:
        project_team_planning_period_system_id = time_sheet_by_date_model.EntityIdField(source="project_team_planning_period_system_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")