# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-16 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Breeze', '0031_registration_nop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accomregistration',
            name='number',
        ),
        migrations.AddField(
            model_name='events',
            name='prizes',
            field=models.CharField(default=b'', help_text=b'prize text for sports', max_length=150),
        ),
    ]
