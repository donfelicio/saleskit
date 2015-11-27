# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0031_reservation_res_manual_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationfilter',
            name='status',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
