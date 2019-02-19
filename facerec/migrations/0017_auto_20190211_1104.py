# Generated by Django 2.1.5 on 2019-02-11 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facerec', '0016_issue_worked_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='Finish_Time',
            field=models.DateTimeField(default='00:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='Start_Time',
            field=models.DateTimeField(default='00:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='Worked_Time',
            field=models.DurationField(default=datetime.timedelta(0), null=True),
        ),
    ]
