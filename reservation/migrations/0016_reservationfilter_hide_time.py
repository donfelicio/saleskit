# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_remove_reservationfilter_hide_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationfilter',
            name='hide_time',
            field=models.TimeField(null=True),
        ),
    ]
