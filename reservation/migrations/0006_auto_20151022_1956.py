# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_auto_20151022_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationfilter',
            old_name='goal_date',
            new_name='hide_days',
        ),
    ]
