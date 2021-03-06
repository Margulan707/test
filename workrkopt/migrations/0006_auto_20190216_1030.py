# Generated by Django 2.1.5 on 2019-02-16 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workrkopt', '0005_auto_20190213_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='Position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='worker', to='workrkopt.Positions'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='Schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workrkopt.Schedules'),
        ),
    ]
