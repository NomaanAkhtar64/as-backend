# Generated by Django 4.0.3 on 2022-04-03 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_attendance_checked_in_attendance_checked_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='checked_in',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
