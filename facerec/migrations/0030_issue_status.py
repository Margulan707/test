# Generated by Django 2.1.5 on 2019-02-11 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facerec', '0029_auto_20190211_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='Status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
