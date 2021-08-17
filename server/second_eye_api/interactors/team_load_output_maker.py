from second_eye_api.models.entities import *
from second_eye_api.models.team_load_output import *
from django.db.models import Sum
import pandas as pd


def delete_old_output(output_database):
    TeamLoadOutputPlanningPeriod.objects.using(output_database).all().delete()

def calculate_tasks_time_left(dedicated_team, skill, system, output_database):
    return Task.objects.using(output_database).filter(
        planning_period=planning_period,
        dedicated_team=dedicated_team,
        skill=skill,
        system=system
    ).aggregate(Sum("time_left"))

def calculate_positions_time_left(dedicated_team, skill, system, output_database):
    return Task.objects.using(output_database).filter(
        planning_period=planning_period,
        dedicated_team=dedicated_team,
        skill=skill,
        system=system
    ).aggregate(Sum("time_left"))

def make_system(team_load_output_skill, skill, system, output_database):
    # team_load_output_system = TeamLoadOutputSystem(
    #     name=system.name,
    #     skill=team_load_output_skill
    # )
    # team_load_output_system.save(using=output_database)

    # print(Task.objects.using(output_database).filter(
    #     skill=skill,
    #     system=system
    # ).aggregate(Sum("estimate")))

    pass

def make_skill(team_load_output_dedicated_team, skill, output_database):
    team_load_output_skill = TeamLoadOutputSkill(
        name=skill.name,
        dedicated_team=team_load_output_dedicated_team
    )
    team_load_output_skill.save(using=output_database)

    systems = System.objects.using(output_database).all()

    for system in systems:
        make_system(team_load_output_skill=team_load_output_skill, skill=skill, system=system, output_database=output_database)

def make_dedicated_team(dedicated_team, team_load_output_planning_period, output_database):
    team_load_output_dedicated_team = TeamLoadOutputDedicatedTeam(
        name=dedicated_team.name,
        planning_period=team_load_output_planning_period
    )
    team_load_output_dedicated_team.save(using=output_database)

    skills = Skill.objects.using(output_database).all()

    for skill in skills:
        make_skill(team_load_output_dedicated_team=team_load_output_dedicated_team, skill=skill, output_database=output_database)

def make_team_load_output_planning_period(planning_period, output_database):
    team_load_output_planning_period = TeamLoadOutputPlanningPeriod(
        id=planning_period.id,
        name=planning_period.name,
        start=planning_period.start,
        end=planning_period.end
    )
    team_load_output_planning_period.save(using=output_database)

    dedicated_teams = planning_period.dedicated_teams.using(output_database).all()

    for dedicated_team in dedicated_teams:
        make_dedicated_team(dedicated_team=dedicated_team, team_load_output_planning_period=team_load_output_planning_period, output_database=output_database)

def make_team_load_outputs(output_data, output_database):
    tasks = output_data.tasks

    pd.set_option('display.max_rows', 500)
    print(tasks.groupby(["planning_period_id", "dedicated_team_id", "skill_id", "system_id"]).agg({"time_left": "sum"}))
    # delete_old_output(output_database=output_database)
    #
    # planning_periods = PlanningPeriod.objects.using(output_database).all()
    #
    # for planning_period in planning_periods:
    #     team_load_output_planning_period = make_team_load_output_planning_period(planning_period=planning_period, output_database=output_database)


