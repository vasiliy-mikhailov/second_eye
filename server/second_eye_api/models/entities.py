from django.db import models

class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    actual_change_request_capacity = models.FloatField()
    time_left = models.FloatField()
    queue_length = models.FloatField()

    actual_analysis_capacity = models.FloatField()
    analysis_time_left = models.FloatField()
    analysis_queue_length = models.FloatField()

    actual_development_capacity = models.FloatField()
    development_time_left = models.FloatField()
    development_queue_length = models.FloatField()

    actual_testing_capacity = models.FloatField()
    testing_time_left = models.FloatField()
    testing_queue_length = models.FloatField()

    def __str__(self):
        return self.name

class DedicatedTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    company = models.ForeignKey(
        "Company", related_name="dedicated_teams", on_delete=models.CASCADE
    )

    actual_change_request_capacity = models.FloatField()
    effort = models.FloatField()
    queue_length = models.FloatField()

    actual_analysis_capacity = models.FloatField()
    analysis_effort = models.FloatField()
    analysis_queue_length = models.FloatField()

    actual_development_capacity = models.FloatField()
    development_effort = models.FloatField()
    development_queue_length = models.FloatField()

    actual_testing_capacity = models.FloatField()
    testing_effort = models.FloatField()
    testing_queue_length = models.FloatField()

    def __str__(self):
        return self.name

class DedicatedTeamPlanningPeriod(models.Model):
    id = models.IntegerField(primary_key=True)
    dedicated_team = models.ForeignKey('DedicatedTeam', db_column='dedicated_team_id', on_delete=models.CASCADE)
    planning_period = models.ForeignKey('PlanningPeriod', db_column='planning_period_id', on_delete=models.CASCADE)
    project_teams = models.ManyToManyField(
        'ProjectTeam', through='ProjectTeamPlanningPeriod', related_name='project_teams'
    )

    estimate = models.FloatField()
    time_spent = models.FloatField()
    time_left = models.FloatField()

class DedicatedTeamPlanningPeriodTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    dedicated_team_planning_period = models.ForeignKey(
        'DedicatedTeamPlanningPeriod', related_name="time_sheets_by_date", on_delete=models.CASCADE
    )

class DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent_with_value_percent_cumsum = models.FloatField()
    time_spent_without_value_percent_cumsum = models.FloatField()

    dedicated_team_planning_period = models.ForeignKey(
        'DedicatedTeamPlanningPeriod', related_name="time_spent_percent_with_value_and_without_value_by_date", on_delete=models.CASCADE
    )

class DedicatedTeamPosition(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    change_request_capacity = models.FloatField(blank=True, null=True)

    dedicated_team = models.ForeignKey(
        'DedicatedTeam', related_name="positions", on_delete=models.CASCADE
    )

    person = models.ForeignKey(
        'Person', related_name="dedicated_team_positions", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name

class DedicatedTeamPositionAbility(models.Model):
    id = models.IntegerField(primary_key=True)
    dedicated_team_position = models.ForeignKey(
        'DedicatedTeamPosition', related_name='abilities', on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        'Skill', related_name='dedicated_team_position_abilities', on_delete=models.CASCADE
    )

    system = models.ForeignKey(
        'System', related_name='dedicated_team_position_abilities', on_delete=models.CASCADE
    )

    def __str__(self):
        return '{} {}'.format(self.skill, self.system)

class ProjectTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    dedicated_team = models.ForeignKey(
        'DedicatedTeam', related_name="project_teams", on_delete=models.CASCADE
    )

    actual_change_request_capacity = models.FloatField()
    effort = models.FloatField()
    queue_length = models.FloatField()

    actual_analysis_capacity = models.FloatField()
    analysis_effort = models.FloatField()
    analysis_queue_length = models.FloatField()

    actual_development_capacity = models.FloatField()
    development_effort = models.FloatField()
    development_queue_length = models.FloatField()

    actual_testing_capacity = models.FloatField()
    testing_effort = models.FloatField()
    testing_queue_length = models.FloatField()

    def __str__(self):
        return self.name

class ProjectTeamPlanningPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    project_team = models.ForeignKey('ProjectTeam', db_column='project_team_id', on_delete=models.CASCADE)
    planning_period = models.ForeignKey('PlanningPeriod', db_column='planning_period_id', on_delete=models.CASCADE)
    dedicated_team_planning_period = models.ForeignKey(
        'DedicatedTeamPlanningPeriod',
        related_name="project_team_planning_periods",
        on_delete=models.CASCADE
    )

    estimate = models.FloatField()
    time_spent = models.FloatField()
    time_left = models.FloatField()

class ProjectTeamPlanningPeriodTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    project_team_planning_period = models.ForeignKey(
        'ProjectTeamPlanningPeriod', related_name="time_sheets_by_date", on_delete=models.CASCADE
    )

class ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent_with_value_percent_cumsum = models.FloatField()
    time_spent_without_value_percent_cumsum = models.FloatField()

    project_team_planning_period = models.ForeignKey(
        'ProjectTeamPlanningPeriod', related_name="time_spent_percent_with_value_and_without_value_by_date", on_delete=models.CASCADE
    )

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    category = models.ForeignKey(
        'StateCategory', related_name="states", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class StateCategory(models.Model):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    NOT_SET = -1

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ChangeRequest(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)

    analysis_express_estimate = models.FloatField(blank=True, null=True)
    development_express_estimate = models.FloatField(blank=True, null=True)
    testing_express_estimate = models.FloatField(blank=True, null=True)
    express_estimate = models.FloatField(blank=True, null=True)

    planned_install_date = models.DateField(blank=True, null=True)

    state = models.ForeignKey(
        'State', related_name="change_requests", on_delete=models.CASCADE
    )

    has_value = models.BooleanField()

    state_category = models.ForeignKey(
        'StateCategory', related_name="change_requests", on_delete=models.CASCADE
    )

    dedicated_team = models.ForeignKey(
        'DedicatedTeam', related_name="change_requests", on_delete=models.CASCADE
    )

    project_team = models.ForeignKey(
        'ProjectTeam', related_name="change_requests", on_delete=models.CASCADE
    )

    planning_period = models.ForeignKey(
        'PlanningPeriod', related_name="change_requests", on_delete=models.CASCADE
    )

    dedicated_team_planning_period = models.ForeignKey(
        'DedicatedTeamPlanningPeriod', related_name='change_requests', on_delete=models.CASCADE
    )

    project_team_planning_period = models.ForeignKey(
        'ProjectTeamPlanningPeriod', related_name='change_requests', on_delete=models.CASCADE
    )

    system_change_requests_analysis_estimate_sum = models.FloatField()
    system_change_requests_development_estimate_sum = models.FloatField()
    system_change_requests_testing_estimate_sum = models.FloatField()
    system_change_requests_estimate_sum = models.FloatField()

    analysis_time_spent = models.FloatField()
    development_time_spent = models.FloatField()
    testing_time_spent = models.FloatField()
    time_spent = models.FloatField()

    analysis_estimate = models.FloatField()
    development_estimate = models.FloatField()
    testing_estimate = models.FloatField()
    estimate = models.FloatField()

    analysis_time_left = models.FloatField()
    development_time_left = models.FloatField()
    testing_time_left = models.FloatField()
    time_left = models.FloatField()

    actual_change_request_capacity = models.FloatField()
    effort = models.FloatField()
    queue_length = models.FloatField()

    actual_analysis_capacity = models.FloatField()
    analysis_effort = models.FloatField()
    analysis_queue_length = models.FloatField()

    actual_development_capacity = models.FloatField()
    development_effort = models.FloatField()
    development_queue_length = models.FloatField()

    actual_testing_capacity = models.FloatField()
    testing_effort = models.FloatField()
    testing_queue_length = models.FloatField()

    def __str__(self):
        return self.name

class System(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SystemChangeRequest(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)

    system = models.ForeignKey(
        'System', related_name="system_change_requests", on_delete=models.CASCADE
    )

    state = models.ForeignKey(
        'State', related_name="system_change_requests", on_delete=models.CASCADE
    )

    has_value = models.BooleanField()

    state_category = models.ForeignKey(
        'StateCategory', related_name="system_change_requests", on_delete=models.CASCADE
    )

    dedicated_team = models.ForeignKey(
        'DedicatedTeam', related_name="system_change_requests", on_delete=models.CASCADE
    )

    project_team = models.ForeignKey(
        'ProjectTeam', related_name="system_change_requests", on_delete=models.CASCADE
    )

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="system_change_requests", on_delete=models.CASCADE
    )

    planning_period = models.ForeignKey(
        'PlanningPeriod', related_name="system_change_requests", on_delete=models.CASCADE
    )

    analysis_preliminary_estimate = models.FloatField(blank=True, null=True)
    development_preliminary_estimate = models.FloatField(blank=True, null=True)
    testing_preliminary_estimate = models.FloatField(blank=True, null=True)

    analysis_planned_estimate = models.FloatField(blank=True, null=True)
    development_planned_estimate = models.FloatField(blank=True, null=True)
    testing_planned_estimate = models.FloatField(blank=True, null=True)

    analysis_tasks_estimate_sum = models.FloatField()
    development_tasks_estimate_sum = models.FloatField()
    testing_tasks_estimate_sum = models.FloatField()
    tasks_estimate_sum = models.FloatField()

    analysis_time_spent = models.FloatField()
    development_time_spent = models.FloatField()
    testing_time_spent = models.FloatField()
    time_spent = models.FloatField()

    analysis_estimate = models.FloatField()
    development_estimate = models.FloatField()
    testing_estimate = models.FloatField()
    estimate = models.FloatField()

    analysis_time_left = models.FloatField()
    development_time_left = models.FloatField()
    testing_time_left = models.FloatField()
    time_left = models.FloatField()

    is_filler = models.BooleanField()

    def __str__(self):
        return self.name

class Skill(models.Model):
    ANALYSIS = 1
    DEVELOPMENT = 2
    TESTING = 3
    NOT_SET = -1
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    preliminary_estimate = models.FloatField(blank=True, null=True)
    planned_estimate = models.FloatField(blank=True, null=True)
    time_spent = models.FloatField(blank=False, null=False)

    skill = models.ForeignKey(
        'Skill', related_name="tasks", on_delete=models.CASCADE
    )

    state = models.ForeignKey(
        'State', related_name="tasks", on_delete=models.CASCADE
    )

    has_value = models.BooleanField()

    state_category = models.ForeignKey(
        'StateCategory', related_name="tasks", on_delete=models.CASCADE
    )

    dedicated_team = models.ForeignKey(
        'DedicatedTeam', related_name="tasks", on_delete=models.CASCADE
    )

    project_team = models.ForeignKey(
        'ProjectTeam', related_name="tasks", on_delete=models.CASCADE
    )

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="tasks", on_delete=models.CASCADE
    )

    system_change_request = models.ForeignKey(
        'SystemChangeRequest', related_name="tasks", on_delete=models.CASCADE
    )

    planning_period = models.ForeignKey(
        'PlanningPeriod', related_name="tasks", on_delete=models.CASCADE
    )

    system = models.ForeignKey(
        "System", related_name="tasks", on_delete=models.CASCADE
    )

    estimate = models.FloatField(blank=False, null=False)
    time_left = models.FloatField(blank=False, null=False)

    def __str__(self):
        return self.name

class FunctionComponentKind(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    function_points = models.IntegerField()

    def __str__(self):
        return self.name

class FunctionComponent(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    count = models.IntegerField()

    state = models.ForeignKey(
        'State', related_name="function_components", on_delete=models.CASCADE
    )

    state_category = models.ForeignKey(
        'StateCategory', related_name="function_components", on_delete=models.CASCADE
    )

    kind = models.ForeignKey(
        'FunctionComponentKind', related_name="function_components", on_delete=models.CASCADE
    )

    kind_function_points = models.IntegerField()

    function_points = models.IntegerField()

    task = models.ForeignKey(
        'Task', related_name="function_components", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class ProjectTeamPosition(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    change_request_capacity = models.FloatField(blank=True, null=True)

    project_team = models.ForeignKey(
        'ProjectTeam', related_name="positions", on_delete=models.CASCADE
    )

    person = models.ForeignKey(
        'Person', related_name="project_team_positions", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Person(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProjectTeamPositionAbility(models.Model):
    id = models.IntegerField(primary_key=True)
    project_team_position = models.ForeignKey(
        'ProjectTeamPosition', related_name='abilities', on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        'Skill', related_name='project_team_position_abilities', on_delete=models.CASCADE
    )

    system = models.ForeignKey(
        'System', related_name='project_team_position_abilities', on_delete=models.CASCADE
    )

    def __str__(self):
        return '{} {}'.format(self.skill, self.system)

class TaskTimeSheets(models.Model):
    id = models.IntegerField(primary_key=True)

    date = models.DateField()

    time_spent = models.FloatField()

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="time_sheets", on_delete=models.CASCADE
    )

    system_change_request = models.ForeignKey(
        'SystemChangeRequest', related_name="time_sheets", on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        'Task', related_name="time_sheets", on_delete=models.CASCADE
    )

    person = models.ForeignKey(
        'Person', related_name="task_time_sheets", on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        "Skill", related_name="time_sheets", on_delete=models.CASCADE
    )

    def __str__(self):
        return '{} {}'.format(self.skill, self.system)

class PlanningPeriod(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    project_teams = models.ManyToManyField(
        'ProjectTeam', through='ProjectTeamPlanningPeriod', related_name='planning_periods'
    )

    dedicated_teams = models.ManyToManyField(
        'DedicatedTeam', through='DedicatedTeamPlanningPeriod', related_name='planning_periods'
    )

    estimate = models.FloatField()
    time_spent = models.FloatField()
    time_left = models.FloatField()

    def __str__(self):
        return self.name

class PlanningPeriodTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    planning_period = models.ForeignKey(
        'PlanningPeriod', related_name="time_sheets_by_date", on_delete=models.CASCADE
    )

class PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent_with_value_percent_cumsum = models.FloatField()
    time_spent_without_value_percent_cumsum = models.FloatField()

    planning_period = models.ForeignKey(
        'PlanningPeriod', related_name="time_spent_percent_with_value_and_without_value_by_date", on_delete=models.CASCADE
    )

class TaskTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    task = models.ForeignKey(
        'Task', related_name="time_sheets_by_date", on_delete=models.CASCADE
    )

class SystemChangeRequestAnalysisTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    system_change_request = models.ForeignKey(
        'SystemChangeRequest', related_name="analysis_time_sheets_by_date", on_delete=models.CASCADE
    )

class SystemChangeRequestDevelopmentTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    system_change_request = models.ForeignKey(
        'SystemChangeRequest', related_name="development_time_sheets_by_date", on_delete=models.CASCADE
    )

class SystemChangeRequestTestingTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    system_change_request = models.ForeignKey(
        'SystemChangeRequest', related_name="testing_time_sheets_by_date", on_delete=models.CASCADE
    )

class SystemChangeRequestTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    system_change_request = models.ForeignKey(
        'SystemChangeRequest', related_name="time_sheets_by_date", on_delete=models.CASCADE
    )


class ChangeRequestAnalysisTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="analysis_time_sheets_by_date", on_delete=models.CASCADE
    )


class ChangeRequestDevelopmentTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="development_time_sheets_by_date", on_delete=models.CASCADE
    )


class ChangeRequestTestingTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="testing_time_sheets_by_date", on_delete=models.CASCADE
    )


class ChangeRequestTimeSheetsByDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    time_spent = models.FloatField()
    time_spent_cumsum = models.FloatField()

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="time_sheets_by_date", on_delete=models.CASCADE
    )

ALL_ENTITIES = [
    Company,
    DedicatedTeam,
    ProjectTeam,
    StateCategory,
    State,
    ChangeRequest,
    SystemChangeRequest,
    Task,
    FunctionComponent,
    FunctionComponentKind,
    Skill,
    System,
    DedicatedTeamPosition,
    ProjectTeamPosition,
    Person,
    DedicatedTeamPositionAbility,
    ProjectTeamPositionAbility,
    TaskTimeSheets,
    PlanningPeriod,
    PlanningPeriodTimeSheetsByDate,
    PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate,
    ProjectTeamPlanningPeriod,
    ProjectTeamPlanningPeriodTimeSheetsByDate,
    ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate,
    DedicatedTeamPlanningPeriod,
    DedicatedTeamPlanningPeriodTimeSheetsByDate,
    DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate,
    TaskTimeSheetsByDate,
    SystemChangeRequestTimeSheetsByDate,
    SystemChangeRequestAnalysisTimeSheetsByDate,
    SystemChangeRequestDevelopmentTimeSheetsByDate,
    SystemChangeRequestTestingTimeSheetsByDate,
    ChangeRequestTimeSheetsByDate,
    ChangeRequestAnalysisTimeSheetsByDate,
    ChangeRequestDevelopmentTimeSheetsByDate,
    ChangeRequestTestingTimeSheetsByDate,
]