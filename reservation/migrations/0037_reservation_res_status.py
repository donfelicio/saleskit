# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0036_reservation_res_total_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_status',
            field=models.CharField(default=b'1', max_length=255),
        ),
    ]
