# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-21 11:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mattersmithapp', '0004_auto_20190121_0621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userm',
            name='roles',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
