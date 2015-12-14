# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0034_reservation_res_assigned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='res_company',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='res_desc',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='res_status',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='res_total_seats',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='res_user',
        ),
    ]
