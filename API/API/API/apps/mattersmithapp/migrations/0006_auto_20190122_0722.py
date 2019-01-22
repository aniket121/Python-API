# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-22 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mattersmithapp', '0005_auto_20190121_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='userm',
            name='is_student',
            field=models.BooleanField(default=False, verbose_name='student status'),
        ),
        migrations.AddField(
            model_name='userm',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='teacher status'),
        ),
    ]
