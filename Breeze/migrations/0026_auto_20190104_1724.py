# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-04 11:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Breeze', '0025_auto_20190104_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('rules', models.CharField(max_length=4000, null=True)),
                ('venue', models.CharField(default='B315', max_length=50)),
                ('date', models.DateField(default='2018-02-09', help_text='Mention (start) date of the event')),
                ('category', models.CharField(choices=[('c', 'cultural'), ('s', 'sports'), ('t', 'technical')], default='c', help_text='category of event eg. Sports, Cultural, Technical', max_length=1)),
                ('subCategory', models.CharField(help_text='In lowercase, without any space. e.g. music, drama', max_length=50)),
                ('subCategoryName', models.CharField(default='', help_text='Proper name of subcategory. eg. Music, Business and Entrepreneurship', max_length=50)),
                ('parentClub', models.CharField(help_text='eg Snuphoria,TEDx,', max_length=50)),
                ('prize', models.DecimalField(decimal_places=2, help_text='Prize Money for the event', max_digits=8, null=True)),
                ('fee', models.DecimalField(decimal_places=2, help_text='Registration fee for the event', max_digits=8, null=True)),
                ('fee_snu', models.DecimalField(decimal_places=2, help_text='Registration fee for the event(SNU Students)', max_digits=8, null=True)),
                ('fee_type', models.CharField(choices=[('head', 'Per Head'), ('team', 'Per Team')], default='head', help_text='type of pricing. Per head or per team', max_length=4)),
                ('min_number', models.DecimalField(decimal_places=0, default=1, help_text='Number of minimum participants', max_digits=2)),
                ('max_number', models.DecimalField(decimal_places=0, default=50, help_text='Number of maximum participants', max_digits=2)),
                ('form_url', models.CharField(default='null', help_text='Google form link. null if no url', max_length=1000)),
                ('form_text', models.CharField(blank=True, default='', help_text='Text to show with Google Form URL in registration successful mail. Leave blank if no url', max_length=1000)),
                ('contact_market', models.CharField(blank=True, help_text='Name of Contact representative', max_length=50)),
                ('phone_market', models.CharField(blank=True, help_text='Contact representative phone number', max_length=10, validators=[django.core.validators.RegexValidator(regex='\\d{10}$')])),
                ('poster_name', models.CharField(blank=True, default='', help_text='Name of poster image file', max_length=100)),
                ('temp', models.CharField(blank=True, default='', help_text='Name of poster image file', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='registration',
            name='eventId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Breeze.Events'),
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]