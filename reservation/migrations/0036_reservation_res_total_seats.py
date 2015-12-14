# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0035_auto_20151214_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_total_seats',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
