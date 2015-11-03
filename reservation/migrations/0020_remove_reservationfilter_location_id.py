# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0019_reservationfilter_location_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationfilter',
            name='location_id',
        ),
    ]
