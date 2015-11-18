# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0025_remove_statuschange_res_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationfilter',
            name='res_id',
        ),
    ]
