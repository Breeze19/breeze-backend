# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-04 11:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Breeze', '0026_auto_20190104_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='temp',
        ),
    ]
