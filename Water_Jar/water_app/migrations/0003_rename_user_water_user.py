# Generated by Django 4.0.4 on 2022-06-27 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('water_app', '0002_rename_user_id_water_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='water',
            old_name='user',
            new_name='User',
        ),
    ]