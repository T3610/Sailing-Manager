# Generated by Django 3.2.6 on 2021-12-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SailingRaceManager', '0008_racer_signedupby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='official',
            name='Role',
            field=models.IntegerField(choices=[(0, 'OOD'), (1, 'AOD'), (2, 'SBH')]),
        ),
    ]