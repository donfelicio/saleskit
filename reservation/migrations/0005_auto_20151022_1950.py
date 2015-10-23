# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_auto_20151022_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationfilter',
            old_name='hide_days',
            new_name='goal_date',
        ),
    ]
