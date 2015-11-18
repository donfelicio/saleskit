# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0022_userprofile_active_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationfilter',
            name='reservation',
            field=models.ForeignKey(default=5539, to='reservation.Reservation'),
            preserve_default=False,
        ),
    ]
