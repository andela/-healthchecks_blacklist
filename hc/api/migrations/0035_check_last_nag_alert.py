# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-21 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_merge_20170221_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='last_nag_alert',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]