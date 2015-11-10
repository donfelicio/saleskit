# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0021_reservationfilter_location_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_reservation',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
