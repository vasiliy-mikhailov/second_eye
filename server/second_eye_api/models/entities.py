


#
# class Task(models.Model):
#     id = models.CharField(primary_key=True, max_length=255)
#     url = models.URLField(max_length=255)
#     name = models.CharField(max_length=255)
#     preliminary_estimate = models.FloatField(blank=True, null=True)
#     planned_estimate = models.FloatField(blank=True, null=True)
#     time_spent = models.FloatField(blank=False, null=False)
#
#     skill = models.ForeignKey(
#         'Skill', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     state = models.ForeignKey(
#         'State', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     has_value = models.BooleanField()
#
#     state_category = models.ForeignKey(
#         'StateCategory', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     dedicated_team = models.ForeignKey(
#         'DedicatedTeam', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     project_team = models.ForeignKey(
#         'ProjectTeam', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     change_request = models.ForeignKey(
#         'ChangeRequest', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     system_change_request = models.ForeignKey(
#         'SystemChangeRequest', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     planning_period = models.ForeignKey(
#         'PlanningPeriod', related_name="tasks", on_delete=models.CASCADE
#     )
#
#     system = models.ForeignKey(
#         "System", related_name="tasks", on_delete=models.CASCADE
#     )
#
#     estimate = models.FloatField(blank=False, null=False)
#     time_left = models.FloatField(blank=False, null=False)
#
#     def __str__(self):
#         return self.name
#
# class FunctionComponentKind(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=255)
#     function_points = models.IntegerField()
#
#     def __str__(self):
#         return self.name
#
# class FunctionComponent(models.Model):
#     id = models.CharField(primary_key=True, max_length=255)
#     url = models.URLField(max_length=255)
#     name = models.CharField(max_length=255)
#     count = models.IntegerField()
#
#     state = models.ForeignKey(
#         'State', related_name="function_components", on_delete=models.CASCADE
#     )
#
#     state_category = models.ForeignKey(
#         'StateCategory', related_name="function_components", on_delete=models.CASCADE
#     )
#
#     kind = models.ForeignKey(
#         'FunctionComponentKind', related_name="function_components", on_delete=models.CASCADE
#     )
#
#     kind_function_points = models.IntegerField()
#
#     function_points = models.IntegerField()
#
#     task = models.ForeignKey(
#         'Task', related_name="function_components", on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return self.name
#
# class ProjectTeamPosition(models.Model):
#     id = models.IntegerField(primary_key=True)
#     url = models.URLField(max_length=255)
#     name = models.CharField(max_length=255)
#     change_request_capacity = models.FloatField(blank=True, null=True)
#
#     project_team = models.ForeignKey(
#         'ProjectTeam', related_name="positions", on_delete=models.CASCADE
#     )
#
#     person = models.ForeignKey(
#         'Person', related_name="project_team_positions", on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return self.name

# class ProjectTeamPositionAbility(models.Model):
#     id = models.IntegerField(primary_key=True)
#     project_team_position = models.ForeignKey(
#         'ProjectTeamPosition', related_name='abilities', on_delete=models.CASCADE
#     )
#
#     skill = models.ForeignKey(
#         'Skill', related_name='project_team_position_abilities', on_delete=models.CASCADE
#     )
#
#     system = models.ForeignKey(
#         'System', related_name='project_team_position_abilities', on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return '{} {}'.format(self.skill, self.system)
#
# class TaskTimeSheets(models.Model):
#     id = models.IntegerField(primary_key=True)
#
#     date = models.DateField()
#
#     time_spent = models.FloatField()
#
#     change_request = models.ForeignKey(
#         'ChangeRequest', related_name="time_sheets", on_delete=models.CASCADE
#     )
#
#     system_change_request = models.ForeignKey(
#         'SystemChangeRequest', related_name="time_sheets", on_delete=models.CASCADE
#     )
#
#     task = models.ForeignKey(
#         'Task', related_name="time_sheets", on_delete=models.CASCADE
#     )
#
#     person = models.ForeignKey(
#         'Person', related_name="task_time_sheets", on_delete=models.CASCADE
#     )
#
#     skill = models.ForeignKey(
#         "Skill", related_name="time_sheets", on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return '{} {}'.format(self.skill, self.system)
#

#
# class TaskTimeSheetsByDate(models.Model):
#     id = models.AutoField(primary_key=True)
#     date = models.DateField()
#
#     time_spent = models.FloatField()
#     time_spent_cumsum = models.FloatField()
#
#     task = models.ForeignKey(
#         'Task', related_name="time_sheets_by_date", on_delete=models.CASCADE
#     )
#
