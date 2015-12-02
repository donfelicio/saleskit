# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0032_reservationfilter_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationfilter',
            name='status',
        ),
    ]
