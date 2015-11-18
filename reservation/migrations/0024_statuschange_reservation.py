# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0023_reservationfilter_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuschange',
            name='reservation',
            field=models.ForeignKey(default=1256, to='reservation.Reservation'),
            preserve_default=False,
        ),
    ]
