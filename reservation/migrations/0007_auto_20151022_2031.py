# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_auto_20151022_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationfilter',
            name='res_id',
            field=models.ForeignKey(to='reservation.Reservation'),
        ),
    ]
