# Generated by Django 3.0.3 on 2020-06-05 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_profile_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile',
            new_name='username',
        ),
    ]
