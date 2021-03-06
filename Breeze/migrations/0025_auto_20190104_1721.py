# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-04 11:51
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Breeze', '0024_auto_20190104_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccomRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.DecimalField(decimal_places=0, max_digits=3, null=True)),
                ('days', models.DecimalField(decimal_places=0, max_digits=1, null=True)),
                ('payable', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('college', models.CharField(default='', max_length=200)),
                ('registration_id', models.CharField(default='', max_length=200, unique=True)),
                ('transaction_status', models.CharField(choices=[('p', 'Paid'), ('u', 'Unpaid')], default='u', max_length=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('fee', models.DecimalField(decimal_places=2, help_text='Fee of the package', max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
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
        migrations.CreateModel(
            name='ForgetPass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Formdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('age', models.IntegerField(default=0, null=True)),
                ('gender', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=18)),
                ('contact', models.CharField(max_length=18)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payable', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('college', models.CharField(default='', max_length=200)),
                ('number_of_participants', models.DecimalField(decimal_places=0, default=0, help_text='0 if not applicable to a event.', max_digits=2)),
                ('registration_id', models.CharField(default='', max_length=200, unique=True)),
                ('transaction_status', models.CharField(choices=[('p', 'Paid'), ('u', 'Unpaid'), ('d', 'Discrepancy')], default='u', max_length=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('eventId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Breeze.Event')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='formdata',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Breeze.Registration'),
        ),
        migrations.AddField(
            model_name='accomregistration',
            name='packageId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Breeze.AccPackage'),
        ),
        migrations.AddField(
            model_name='accomregistration',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
