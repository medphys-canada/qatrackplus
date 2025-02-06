# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 15:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0003_auto_20171204_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='date_acceptance',
            field=models.DateField(default=datetime.datetime(2018, 1, 1, 12, 0, 0, 0, tzinfo=datetime.timezone.utc), help_text='Optional date of acceptance'),
            preserve_default=False,
        ),
    ]
