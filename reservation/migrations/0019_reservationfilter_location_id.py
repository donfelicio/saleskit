# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0018_auto_20151102_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationfilter',
            name='location_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
