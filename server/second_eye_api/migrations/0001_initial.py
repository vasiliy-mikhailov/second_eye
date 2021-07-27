# Generated by Django 3.2.5 on 2021-07-26 15:27

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
            ],
        ),
        migrations.CreateModel(
            name='DedicatedTeam',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FunctionComponentType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('weight', models.IntegerField()),
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
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.skill')),
                ('system_change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='second_eye_api.changerequest')),
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
            name='ProjectTeam',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('dedicated_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_teams', to='second_eye_api.dedicatedteam')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionComponent',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('function_component_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.functioncomponenttype')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_components', to='second_eye_api.task')),
            ],
        ),
        migrations.AddField(
            model_name='changerequest',
            name='project_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_requests', to='second_eye_api.projectteam'),
        ),
    ]
