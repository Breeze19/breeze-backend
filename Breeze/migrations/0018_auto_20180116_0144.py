# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-15 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Breeze', '0017_auto_20180115_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomregistration',
            name='remarks',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='registration',
            name='remarks',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
