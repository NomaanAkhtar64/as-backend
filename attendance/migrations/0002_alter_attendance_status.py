# Generated by Django 3.2.12 on 2022-04-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('Paid Leave', 'Paid Leave'), ('Present', 'Present')], default='Present', max_length=10),
        ),
    ]
