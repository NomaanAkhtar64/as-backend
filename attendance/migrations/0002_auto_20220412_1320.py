# Generated by Django 3.2.12 on 2022-04-12 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='updated_at',
        ),
    ]