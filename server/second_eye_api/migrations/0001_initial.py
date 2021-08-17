# Generated by Django 3.2.6 on 2021-08-17 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeRequest',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('analysis_express_estimate', models.FloatField(blank=True, null=True)),
                ('development_express_estimate', models.FloatField(blank=True, null=True)),
                ('testing_express_estimate', models.FloatField(blank=True, null=True)),
                ('express_estimate', models.FloatField(blank=True, null=True)),
                ('planned_install_date', models.DateField(blank=True, null=True)),
                ('has_value', models.BooleanField()),
                ('system_change_requests_analysis_estimate_sum', models.FloatField()),
                ('system_change_requests_development_estimate_sum', models.FloatField()),
                ('system_change_requests_testing_estimate_sum', models.FloatField()),
                ('system_change_requests_estimate_sum', models.FloatField()),
                ('analysis_time_spent', models.FloatField()),
                ('development_time_spent', models.FloatField()),
                ('testing_time_spent', models.FloatField()),
                ('time_spent', models.FloatField()),
                ('analysis_estimate', models.FloatField()),
                ('development_estimate', models.FloatField()),
                ('testing_estimate', models.FloatField()),
                ('estimate', models.FloatField()),
                ('analysis_time_left', models.FloatField()),
                ('development_time_left', models.FloatField()),
                ('testing_time_left', models.FloatField()),
                ('time_left', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DedicatedTeam',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DedicatedTeamPlanningPeriod',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('estimate', models.FloatField()),
                ('time_spent', models.FloatField()),
                ('time_left', models.FloatField()),
                ('dedicated_team', models.ForeignKey(db_column='dedicated_team_id', on_delete=django.db.models.deletion.CASCADE, to='second_eye_api.dedicatedteam')),
            ],
        ),
        migrations.CreateModel(
            name='DedicatedTeamPosition',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('change_request_capacity', models.FloatField(blank=True, null=True)),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='second_eye_api.dedicatedteam')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionComponentKind',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('function_points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PlanningPeriod',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('dedicated_teams', models.ManyToManyField(related_name='planning_periods', through='second_eye_api.DedicatedTeamPlanningPeriod', to='second_eye_api.DedicatedTeam')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_teams', to='second_eye_api.dedicatedteam')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTeamPosition',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('change_request_capacity', models.FloatField(blank=True, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_team_positions', to='second_eye_api.person')),
                ('project_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='second_eye_api.projectteam')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StateCategory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SystemChangeRequest',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('has_value', models.BooleanField()),
                ('analysis_preliminary_estimate', models.FloatField(blank=True, null=True)),
                ('development_preliminary_estimate', models.FloatField(blank=True, null=True)),
                ('testing_preliminary_estimate', models.FloatField(blank=True, null=True)),
                ('analysis_planned_estimate', models.FloatField(blank=True, null=True)),
                ('development_planned_estimate', models.FloatField(blank=True, null=True)),
                ('testing_planned_estimate', models.FloatField(blank=True, null=True)),
                ('analysis_tasks_estimate_sum', models.FloatField()),
                ('development_tasks_estimate_sum', models.FloatField()),
                ('testing_tasks_estimate_sum', models.FloatField()),
                ('tasks_estimate_sum', models.FloatField()),
                ('analysis_time_spent', models.FloatField()),
                ('development_time_spent', models.FloatField()),
                ('testing_time_spent', models.FloatField()),
                ('time_spent', models.FloatField()),
                ('analysis_estimate', models.FloatField()),
                ('development_estimate', models.FloatField()),
                ('testing_estimate', models.FloatField()),
                ('estimate', models.FloatField()),
                ('analysis_time_left', models.FloatField()),
                ('development_time_left', models.FloatField()),
                ('testing_time_left', models.FloatField()),
                ('time_left', models.FloatField()),
                ('is_filler', models.BooleanField()),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.changerequest')),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.dedicatedteam')),
                ('planning_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.planningperiod')),
                ('project_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.projectteam')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.state')),
                ('state_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.statecategory')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.system')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('preliminary_estimate', models.FloatField(blank=True, null=True)),
                ('planned_estimate', models.FloatField(blank=True, null=True)),
                ('time_spent', models.FloatField()),
                ('has_value', models.BooleanField()),
                ('estimate', models.FloatField()),
                ('time_left', models.FloatField()),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.changerequest')),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.dedicatedteam')),
                ('planning_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.planningperiod')),
                ('project_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.projectteam')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.skill')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.state')),
                ('state_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.statecategory')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.system')),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.systemchangerequest')),
            ],
        ),
        migrations.CreateModel(
            name='TeamLoadOutputDedicatedTeam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TeamLoadOutputPlanningPeriod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TeamLoadOutputSkill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='second_eye_api.teamloadoutputdedicatedteam')),
            ],
        ),
        migrations.CreateModel(
            name='TeamLoadOutputSystem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('capacity_left', models.FloatField()),
                ('effort_left', models.FloatField()),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='systems', to='second_eye_api.teamloadoutputskill')),
            ],
        ),
        migrations.AddField(
            model_name='teamloadoutputdedicatedteam',
            name='planning_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dedicated_teams', to='second_eye_api.teamloadoutputplanningperiod'),
        ),
        migrations.CreateModel(
            name='TaskTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets_by_date', to='second_eye_api.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskTimeSheets',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets', to='second_eye_api.changerequest')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_time_sheets', to='second_eye_api.person')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets', to='second_eye_api.skill')),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets', to='second_eye_api.systemchangerequest')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets', to='second_eye_api.task')),
            ],
        ),
        migrations.CreateModel(
            name='SystemChangeRequestTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets_by_date', to='second_eye_api.systemchangerequest')),
            ],
        ),
        migrations.CreateModel(
            name='SystemChangeRequestTestingTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testing_time_sheets_by_date', to='second_eye_api.systemchangerequest')),
            ],
        ),
        migrations.CreateModel(
            name='SystemChangeRequestDevelopmentTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='development_time_sheets_by_date', to='second_eye_api.systemchangerequest')),
            ],
        ),
        migrations.CreateModel(
            name='SystemChangeRequestAnalysisTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis_time_sheets_by_date', to='second_eye_api.systemchangerequest')),
            ],
        ),
        migrations.AddField(
            model_name='state',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='second_eye_api.statecategory'),
        ),
        migrations.CreateModel(
            name='ProjectTeamPositionAbility',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_team_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abilities', to='second_eye_api.projectteamposition')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_team_position_abilities', to='second_eye_api.skill')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_team_position_abilities', to='second_eye_api.system')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTeamPlanningPeriod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('planning_period', models.ForeignKey(db_column='planning_period_id', on_delete=django.db.models.deletion.CASCADE, to='second_eye_api.planningperiod')),
                ('project_team', models.ForeignKey(db_column='project_team_id', on_delete=django.db.models.deletion.CASCADE, to='second_eye_api.projectteam')),
            ],
        ),
        migrations.AddField(
            model_name='planningperiod',
            name='project_teams',
            field=models.ManyToManyField(related_name='planning_periods', through='second_eye_api.ProjectTeamPlanningPeriod', to='second_eye_api.ProjectTeam'),
        ),
        migrations.CreateModel(
            name='FunctionComponent',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('count', models.IntegerField()),
                ('kind_function_points', models.IntegerField()),
                ('function_points', models.IntegerField()),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.functioncomponentkind')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.state')),
                ('state_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.statecategory')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.task')),
            ],
        ),
        migrations.CreateModel(
            name='DedicatedTeamPositionAbility',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dedicated_team_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abilities', to='second_eye_api.dedicatedteamposition')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dedicated_team_position_abilities', to='second_eye_api.skill')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dedicated_team_position_abilities', to='second_eye_api.system')),
            ],
        ),
        migrations.AddField(
            model_name='dedicatedteamposition',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dedicated_team_positions', to='second_eye_api.person'),
        ),
        migrations.CreateModel(
            name='DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent_with_value_percent_cumsum', models.FloatField()),
                ('time_spent_without_value_percent_cumsum', models.FloatField()),
                ('dedicated_team_planning_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_spent_percent_with_value_and_without_value_by_date', to='second_eye_api.dedicatedteamplanningperiod')),
            ],
        ),
        migrations.CreateModel(
            name='DedicatedTeamPlanningPeriodTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('dedicated_team_planning_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets_by_date', to='second_eye_api.dedicatedteamplanningperiod')),
            ],
        ),
        migrations.AddField(
            model_name='dedicatedteamplanningperiod',
            name='planning_period',
            field=models.ForeignKey(db_column='planning_period_id', on_delete=django.db.models.deletion.CASCADE, to='second_eye_api.planningperiod'),
        ),
        migrations.CreateModel(
            name='ChangeRequestTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_sheets_by_date', to='second_eye_api.changerequest')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRequestTestingTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testing_time_sheets_by_date', to='second_eye_api.changerequest')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRequestDevelopmentTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='development_time_sheets_by_date', to='second_eye_api.changerequest')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRequestAnalysisTimeSheetsByDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('time_spent_cumsum', models.FloatField()),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis_time_sheets_by_date', to='second_eye_api.changerequest')),
            ],
        ),
        migrations.AddField(
            model_name='changerequest',
            name='dedicated_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.dedicatedteam'),
        ),
        migrations.AddField(
            model_name='changerequest',
            name='dedicated_team_planning_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.dedicatedteamplanningperiod'),
        ),
        migrations.AddField(
            model_name='changerequest',
            name='planning_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.planningperiod'),
        ),
        migrations.AddField(
            model_name='changerequest',
            name='project_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.projectteam'),
        ),
        migrations.AddField(
            model_name='changerequest',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.state'),
        ),
        migrations.AddField(
            model_name='changerequest',
            name='state_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.statecategory'),
        ),
    ]