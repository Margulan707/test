# Generated by Django 2.1.5 on 2019-02-11 18:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facerec', '0027_auto_20190211_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='Early_Leave',
            field=models.DurationField(default=datetime.timedelta(0), null=True),
        ),
        migrations.AlterField(
            model_name='day',
            name='Late_Come',
            field=models.DurationField(default=datetime.timedelta(0), null=True),
        ),
    ]
