# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0010_reservation_res_last_step_before_cancel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='res_last_step_before_cancel',
            new_name='res_prev_status',
        ),
    ]
