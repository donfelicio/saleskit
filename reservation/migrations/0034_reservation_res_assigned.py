# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0033_remove_reservationfilter_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_assigned',
            field=models.CharField(default=b'no', max_length=255),
        ),
    ]
