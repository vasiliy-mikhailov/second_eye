from django.db import models

class DedicatedTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProjectTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    dedicated_team = models.ForeignKey(
        'DedicatedTeam', related_name="project_teams", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class ChangeRequest(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    express_estimate = models.FloatField(blank=True, null=True)

    project_team = models.ForeignKey(
        'ProjectTeam', related_name="change_requests", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class System(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SystemChangeRequest(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)

    system = models.ForeignKey(
        'System', related_name="system_change_requests", on_delete=models.CASCADE
    )

    change_request = models.ForeignKey(
        'ChangeRequest', related_name="system_change_requests", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Skill(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    skill = models.ForeignKey(
        'Skill', related_name="tasks", on_delete=models.CASCADE
    )

    system_change_request = models.ForeignKey(
        'SystemChangeRequest', related_name="tasks", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class FunctionComponentKind(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    weight = models.IntegerField()

    def __str__(self):
        return self.name

class FunctionComponent(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)

    function_component_kind = models.ForeignKey(
        'FunctionComponentKind', related_name="function_components", on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        'Task', related_name="function_components", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

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