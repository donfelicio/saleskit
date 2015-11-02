# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_auto_20151031_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationfilter',
            name='hide_time',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
