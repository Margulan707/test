# Generated by Django 2.1.5 on 2019-02-07 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workrkopt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedules',
            name='Fri',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriBr1',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriBr1In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriBr1Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriBr2',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriBr2In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriBr2Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriIn',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='FriOut',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='Mon',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonBr1',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonBr1In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonBr1Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonBr2',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonBr2In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonBr2Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonIn',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='MonOut',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='Sat',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatBr1',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatBr1In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatBr1Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatBr2',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatBr2In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatBr2Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatIn',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SatOut',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='Sun',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunBr1',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunBr1In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunBr1Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunBr2',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunBr2In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunBr2Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunIn',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='SunOut',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='Thu',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuBr1',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuBr1In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuBr1Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuBr2',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuBr2In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuBr2Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuIn',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='ThuOut',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='Tue',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueBr1',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueBr1In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueBr1Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueBr2',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueBr2In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueBr2Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueIn',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='TueOut',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='Wed',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedBr1',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedBr1In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedBr1Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedBr2',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedBr2In',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedBr2Out',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedIn',
        ),
        migrations.RemoveField(
            model_name='schedules',
            name='WedOut',
        ),
        migrations.AddField(
            model_name='schedules',
            name='Friday',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedules',
            name='Monday',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedules',
            name='Saturday',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedules',
            name='Sunday',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedules',
            name='Thursday',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedules',
            name='Tuesday',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedules',
            name='Wednesday',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]