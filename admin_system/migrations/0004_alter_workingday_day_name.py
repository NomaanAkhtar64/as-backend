# Generated by Django 3.2.12 on 2022-04-16 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_system', '0003_auto_20220416_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingday',
            name='day_name',
            field=models.CharField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], max_length=2, unique=True),
        ),
    ]