# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-14 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20170214_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='set_nag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='check',
            name='nag_interval',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
