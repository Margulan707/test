# Generated by Django 2.1.5 on 2019-02-11 17:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facerec', '0018_issue_solved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='Worked_Time',
            field=models.DurationField(default=datetime.timedelta(0), null=True),
        ),
    ]
