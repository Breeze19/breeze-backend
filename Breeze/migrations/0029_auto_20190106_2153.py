# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-06 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Breeze', '0028_profile_college'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='number_of_participants',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='payable',
        ),
    ]