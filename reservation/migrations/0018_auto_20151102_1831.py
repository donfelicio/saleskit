# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0017_remove_reservationfilter_hide_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationfilter',
            name='hide_hour',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='reservationfilter',
            name='hide_minute',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
