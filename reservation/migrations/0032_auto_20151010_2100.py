# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0031_reservation_res_last_action_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_last_action_taken',
            field=models.DateField(default=datetime.date(2015, 10, 10), auto_now_add=True),
            preserve_default=False,
        ),
    ]
