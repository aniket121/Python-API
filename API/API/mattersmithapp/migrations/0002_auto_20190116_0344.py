# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-16 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mattersmithapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(1, 'student'), (2, 'teacher'), (3, 'secretary'), (4, 'supervisor'), (5, 'admin')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='userm',
            name='roles',
            field=models.ManyToManyField(to='mattersmithapp.Role'),
        ),
    ]
