# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_auto_20151022_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationfilter',
            name='res_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
