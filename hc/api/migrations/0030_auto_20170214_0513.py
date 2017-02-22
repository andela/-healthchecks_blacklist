# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-14 05:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20170213_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='nag',
        ),
        migrations.AddField(
            model_name='check',
            name='nag_interval',
            field=models.DurationField(default=datetime.timedelta(0, 1800)),
        ),
    ]
