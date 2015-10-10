# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0025_reservation_res_location_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_date_created',
            field=models.DateField(),
        ),
    ]
