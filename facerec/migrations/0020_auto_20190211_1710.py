# Generated by Django 2.1.5 on 2019-02-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facerec', '0019_auto_20190211_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='Worked_Time',
            field=models.TimeField(default='00:00:00', null=True),
        ),
    ]
