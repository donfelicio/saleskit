# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_userprofile_loc_updated'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hidereservation',
            new_name='Reservationfilter',
        ),
    ]
