import cubista
import datetime

from .. import project_team_quarter_system
from .. import quarter
from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class ProjectTeamQuarterSystemTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["project_team_quarter_system_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_quarter_system_id = cubista.AggregatedTableGroupField(source="project_team_quarter_system_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["project_team_quarter_system_id"], sort_by=["date"])

        dedicated_team_quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter_system.ProjectTeamQuarterSystem,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_quarter_id",
            default=-1
        )

        project_team_quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter_system.ProjectTeamQuarterSystem,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="project_team_quarter_id",
            default=-1
        )

        quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter_system.ProjectTeamQuarterSystem,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="quarter_id",
            default=-1
        )

        quarter_start = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.date.today()
        )

        quarter_end = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.date.today()
        )

        dedicated_team_quarter_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter_system.ProjectTeamQuarterSystem,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_quarter_system_id",
            default=-1
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["project_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["project_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["project_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["project_team_quarter_system_id"],
            foreign_field_names=["project_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: utils.normalize(
                x=x["date"], min_x=x["time_sheets_by_date_model_min_date"],
                max_x=x["time_sheets_by_date_model_max_date"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class ProjectTeamQuarterSystemTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: ProjectTeamQuarterSystemTimeSheetByDate
        entity_id_field_name = "project_team_quarter_system_id"

    class Fields:
        project_team_quarter_system_id = time_sheet_by_date_model.EntityIdField(source="project_team_quarter_system_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")