# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0017_auto_20151015_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_10',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_11',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_3',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_4',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_5',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_6',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_7',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_8',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='filter_9',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_login',
            field=models.DateField(null=True),
        ),
    ]
