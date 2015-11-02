# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0016_reservationfilter_hide_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationfilter',
            name='hide_time',
        ),
    ]
