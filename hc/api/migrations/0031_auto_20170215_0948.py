# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-15 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20170215_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='nag',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='check',
            name='nag_after',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]