# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-15 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170215_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reports_allowed',
            field=models.IntegerField(default=0),
        ),
    ]
