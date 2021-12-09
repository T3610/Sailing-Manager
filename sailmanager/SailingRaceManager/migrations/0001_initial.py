# Generated by Django 3.2.6 on 2021-09-27 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BoatName', models.CharField(max_length=50)),
                ('PyNumber', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RaceNumber', models.PositiveIntegerField(unique=True)),
                ('StartTime', models.TimeField(blank=True, null=True)),
                ('RaceLength', models.PositiveIntegerField(default=40)),
                ('RaceType', models.IntegerField(choices=[(0, 'Handicap'), (1, 'Pursuit')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Racer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HelmName', models.CharField(max_length=50)),
                ('CrewName', models.CharField(blank=True, max_length=50, null=True)),
                ('SailNumber', models.CharField(max_length=50)),
                ('Boat', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Boat', to='SailingRaceManager.boat')),
            ],
        ),
        migrations.CreateModel(
            name='RaceEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LapsComplete', models.PositiveIntegerField(default=0)),
                ('FinishTime', models.DateTimeField(blank=True, null=True)),
                ('Status', models.IntegerField(blank=True, choices=[(0, 'FINISHED'), (1, 'RETIRED'), (2, 'DID NOT START')], null=True)),
                ('Race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Race', to='SailingRaceManager.race')),
                ('Racer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Racer', to='SailingRaceManager.racer')),
            ],
        ),
    ]