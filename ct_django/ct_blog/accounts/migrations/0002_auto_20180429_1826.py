# Generated by Django 2.0.3 on 2018-04-29 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='times',
            new_name='timestamp',
        ),
    ]
