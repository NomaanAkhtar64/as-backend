# Generated by Django 3.2.12 on 2022-04-19 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('attendance', '0003_leaves'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Leaves',
            new_name='Leave',
        ),
    ]