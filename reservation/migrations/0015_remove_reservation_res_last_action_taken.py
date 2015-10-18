# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0014_reservation_res_last_change_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='res_last_action_taken',
        ),
    ]
