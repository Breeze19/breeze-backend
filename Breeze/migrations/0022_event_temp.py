# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-04 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Breeze', '0021_event_fee_snu'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='temp',
            field=models.CharField(blank=True, default='', help_text='Name of poster image file', max_length=100),
        ),
    ]