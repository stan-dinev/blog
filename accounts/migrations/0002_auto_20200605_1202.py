# Generated by Django 3.0.3 on 2020-06-05 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone_number',
            new_name='age',
        ),
    ]