# Generated by Django 3.2.6 on 2021-11-25 10:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SailingRaceManager', '0006_auto_20211125_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='Date',
            field=models.DateField(default=datetime.datetime(2021, 11, 25, 10, 28, 26, 944835)),
            preserve_default=False,
        ),
    ]