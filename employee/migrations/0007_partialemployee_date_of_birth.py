# Generated by Django 3.2.12 on 2022-04-15 09:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20220415_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='partialemployee',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2022, 4, 15)),
            preserve_default=False,
        ),
    ]