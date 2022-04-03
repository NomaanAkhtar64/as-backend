# Generated by Django 4.0.3 on 2022-04-01 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Paid Leave', 'Paid Leave'), ('Present', 'Present')], max_length=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.employee')),
            ],
        ),
    ]