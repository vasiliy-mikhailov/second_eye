# Generated by Django 3.2.5 on 2021-08-01 15:42

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
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('express_estimate', models.FloatField(blank=True, null=True)),
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
            name='FunctionComponentKind',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('weight', models.IntegerField()),
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
            name='ProjectTeam',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_teams', to='second_eye_api.dedicatedteam')),
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
            name='System',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SystemChangeRequest',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.changerequest')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_change_requests', to='second_eye_api.system')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.skill')),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.systemchangerequest')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTeamPosition',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('new_function_capacity', models.FloatField(blank=True, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_team_positions', to='second_eye_api.person')),
                ('project_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='second_eye_api.projectteam')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionComponent',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('function_component_kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.functioncomponentkind')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.task')),
            ],
        ),
        migrations.CreateModel(
            name='DedicatedTeamPosition',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('new_function_capacity', models.FloatField(blank=True, null=True)),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='second_eye_api.dedicatedteam')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dedicated_team_positions', to='second_eye_api.person')),
            ],
        ),
        migrations.AddField(
            model_name='changerequest',
            name='project_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.projectteam'),
        ),
    ]
