# Generated by Django 4.0.3 on 2022-04-03 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('repeats', models.CharField(choices=[('Yearly', 'Yearly'), ('Monthly', 'Monthly'), ('Once', 'Once')], max_length=32)),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('Half Day', 'Half Day'), ('Full Day', 'Full Day')], max_length=32)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
            ],
        ),
    ]
