# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-16 05:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mattersmithapp', '0002_auto_20190116_0344'),
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