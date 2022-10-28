import cubista

from . import dedicated_team
from . import dedicated_team_planning_period
from . import incident
from . import project_team
from . import project_team_planning_period
from . import skill
from . import state
from . import time_sheet

class IncidentSubTask(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        skill_id = cubista.ForeignKeyField(foreign_table=lambda: skill.Skill, default=-1, nulls=False)
        time_left = cubista.FloatField(nulls=False)
        time_original_estimate = cubista.FloatField(nulls=False)
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default="-1", nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        incident_id = cubista.ForeignKeyField(
            foreign_table=lambda: incident.Incident,
            default=-1,
            nulls=False
        )

        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="project_team_id")
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="project_manager_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="dedicated_team_id")

        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: incident.Incident, related_field_name="incident_id", pulled_field_name="company_id")

        planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: incident.Incident,
            related_field_name="incident_id",
            pulled_field_name="planning_period_id"
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_id", "planning_period_id"],
            foreign_field_names=["project_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
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

        time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: time_sheet.IncidentSubTaskTimeSheet,
            foreign_field_name="incident_sub_task_id",
            aggregated_field_name="time_spent",
            aggregate_function="sum",
            default=0
        )

