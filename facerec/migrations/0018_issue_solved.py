# Generated by Django 2.1.5 on 2019-02-10 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facerec', '0017_auto_20190211_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='Solved',
            field=models.BooleanField(default=False),
        ),
    ]