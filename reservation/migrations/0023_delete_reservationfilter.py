# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0022_userprofile_active_reservation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reservationfilter',
        ),
    ]
