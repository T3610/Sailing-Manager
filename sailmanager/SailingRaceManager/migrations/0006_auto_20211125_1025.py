# Generated by Django 3.2.6 on 2021-11-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SailingRaceManager', '0005_alter_race_starttime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Official',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role', models.CharField(choices=[(0, 'OOD'), (1, 'AOD'), (2, 'SBH')], max_length=50)),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='RaceNumber',
            field=models.PositiveIntegerField(),
        ),
    ]
