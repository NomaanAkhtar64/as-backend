# Generated by Django 4.0.3 on 2022-04-03 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_rename_name_employee_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='mac_address',
            field=models.CharField(blank=True, max_length=17, unique=True),
        ),
    ]
