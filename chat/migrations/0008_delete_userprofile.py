# Generated by Django 3.0.3 on 2020-06-18 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]