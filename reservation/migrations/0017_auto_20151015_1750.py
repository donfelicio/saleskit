# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0016_auto_20151015_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hidereservation',
            name='hide_days',
            field=models.DateField(null=True),
        ),
    ]
