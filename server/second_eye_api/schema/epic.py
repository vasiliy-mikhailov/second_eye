import graphene_frame
from . import change_request
from . import company
from . import person
from . import system
from . import system_change_request

class Epic(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()

        company = graphene_frame.Field(to_entity=lambda: company.Company)

        systems = graphene_frame.List(
            to_entity=lambda: EpicSystem,
            to_field="epic_id"
        )

        change_requests = graphene_frame.List(
            to_entity=lambda: change_request.ChangeRequest,
            to_field="epic_id"
        )

        analysis_time_spent = graphene_frame.Float()
        development_time_spent = graphene_frame.Float()
        testing_time_spent = graphene_frame.Float()
        time_spent = graphene_frame.Float()

        analysis_estimate = graphene_frame.Float()
        development_estimate = graphene_frame.Float()
        testing_estimate = graphene_frame.Float()
        estimate = graphene_frame.Float()

        analysis_time_left = graphene_frame.Float()
        development_time_left = graphene_frame.Float()
        testing_time_left = graphene_frame.Float()
        time_left = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        persons = graphene_frame.List(to_entity=lambda: person.PersonEpicTimeSpent, to_field="epic_id")

        analysis_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: EpicAnalysisTimeSheetsByDate,
            to_field="epic_id"
        )

        development_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: EpicDevelopmentTimeSheetsByDate,
            to_field="epic_id"
        )

        testing_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: EpicTestingTimeSheetsByDate,
            to_field="epic_id"
        )

        time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: EpicTimeSheetsByDate,
            to_field="epic_id"
        )

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

    def __str__(self):
        return self.name

class EpicAnalysisTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        epic = graphene_frame.Field(to_entity=lambda: Epic)

class EpicDevelopmentTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        epic = graphene_frame.Field(to_entity=lambda: Epic)

class EpicTestingTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        epic = graphene_frame.Field(to_entity=lambda: Epic)

class EpicTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        epic = graphene_frame.Field(to_entity=lambda: Epic)

class EpicSystem(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        epic = graphene_frame.Field(to_entity=lambda: Epic)
        epic_key = graphene_frame.String()

        system = graphene_frame.Field(to_entity=lambda: system.System)

        system_change_requests = graphene_frame.List(
            to_entity=lambda: system_change_request.SystemChangeRequest,
            to_field="epic_system_id"
        )

        analysis_time_spent = graphene_frame.Float()
        development_time_spent = graphene_frame.Float()
        testing_time_spent = graphene_frame.Float()
        time_spent = graphene_frame.Float()

        analysis_estimate = graphene_frame.Float()
        development_estimate = graphene_frame.Float()
        testing_estimate = graphene_frame.Float()
        estimate = graphene_frame.Float()

        analysis_time_left = graphene_frame.Float()
        development_time_left = graphene_frame.Float()
        testing_time_left = graphene_frame.Float()
        time_left = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: EpicSystemTimeSheetsByDate,
            to_field="epic_system_id"
        )

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

    def __str__(self):
        return self.name

class EpicSystemTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        epic_system = graphene_frame.Field(to_entity=lambda: EpicSystem)