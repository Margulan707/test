# Generated by Django 2.1.5 on 2019-02-08 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facerec', '0007_remove_workshift_current'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='Last_Check_In',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Status',
        ),
        migrations.AlterField(
            model_name='check',
            name='WorkShift',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='facerec.WorkShift'),
        ),
    ]
