# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-04 11:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Breeze', '0022_event_temp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='temp',
        ),
    ]
