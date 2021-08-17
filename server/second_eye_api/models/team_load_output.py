from django.db import models

class TeamLoadOutputPlanningPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name

class TeamLoadOutputDedicatedTeam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    planning_period = models.ForeignKey(
        TeamLoadOutputPlanningPeriod, related_name="dedicated_teams", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class TeamLoadOutputSkill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    dedicated_team = models.ForeignKey(
        TeamLoadOutputDedicatedTeam, related_name="skills", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class TeamLoadOutputSystem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    skill = models.ForeignKey(
        TeamLoadOutputSkill, related_name="systems", on_delete=models.CASCADE
    )

    capacity_left = models.FloatField()
    effort_left = models.FloatField()

    def __str__(self):
        return self.name

ALL_TEAM_LOAD_OUTPUTS = [
    TeamLoadOutputPlanningPeriod,
    TeamLoadOutputDedicatedTeam,
    TeamLoadOutputSkill,
    TeamLoadOutputSystem,
]