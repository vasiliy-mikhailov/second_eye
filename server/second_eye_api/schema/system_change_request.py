import graphene_frame
from . import system
from . import state
from . import state_category
from . import dedicated_team
from . import project_team
from . import change_request
from . import planning_period
from . import task

class SystemChangeRequest(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.String())
        url = graphene_frame.String()
        name = graphene_frame.String()

        system = graphene_frame.Field(to_entity=lambda: system.System)

        state = graphene_frame.Field(to_entity=lambda: state.State)

        has_value = graphene_frame.Boolean()

        state_category = graphene_frame.Field(to_entity=lambda: state_category.StateCategory)

        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)

        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)

        change_request = graphene_frame.Field(to_entity=lambda: change_request.ChangeRequest)

        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)

        analysis_preliminary_estimate = graphene_frame.Float(nulls=True)
        development_preliminary_estimate = graphene_frame.Float(nulls=True)
        testing_preliminary_estimate = graphene_frame.Float(nulls=True)

        analysis_planned_estimate = graphene_frame.Float(nulls=True)
        development_planned_estimate = graphene_frame.Float(nulls=True)
        testing_planned_estimate = graphene_frame.Float(nulls=True)

        analysis_tasks_estimate_sum = graphene_frame.Float()
        development_tasks_estimate_sum = graphene_frame.Float()
        testing_tasks_estimate_sum = graphene_frame.Float()
        tasks_estimate_sum = graphene_frame.Float()

        analysis_time_spent = graphene_frame.Float()
        development_time_spent = graphene_frame.Float()
        testing_time_spent = graphene_frame.Float()
        time_spent = graphene_frame.Float()

        analysis_estimate = graphene_frame.Float()
        development_estimate = graphene_frame.Float()
        testing_estimate =graphene_frame.Float()
        estimate = graphene_frame.Float()

        analysis_time_left = graphene_frame.Float()
        development_time_left = graphene_frame.Float()
        testing_time_left = graphene_frame.Float()
        time_left = graphene_frame.Float()

        is_filler = graphene_frame.Boolean()

        tasks = graphene_frame.List(
            to_entity=lambda: task.Task,
            to_field='system_change_request_id'
        )

        analysis_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: SystemChangeRequestAnalysisTimeSheetsByDate,
            to_field='system_change_request_id'
        )

        development_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: SystemChangeRequestDevelopmentTimeSheetsByDate,
            to_field='system_change_request_id'
        )

        testing_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: SystemChangeRequestTestingTimeSheetsByDate,
            to_field='system_change_request_id'
        )

        time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: SystemChangeRequestTimeSheetsByDate,
            to_field='system_change_request_id'
        )

    def __str__(self):
        return self.name

class SystemChangeRequestAnalysisTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        system_change_request = graphene_frame.Field(to_entity=lambda: SystemChangeRequest)

class SystemChangeRequestDevelopmentTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        system_change_request = graphene_frame.Field(to_entity=lambda: SystemChangeRequest)

class SystemChangeRequestTestingTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        system_change_request = graphene_frame.Field(to_entity=lambda: SystemChangeRequest)

class SystemChangeRequestTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        system_change_request = graphene_frame.Field(to_entity=lambda: SystemChangeRequest)

