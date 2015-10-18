# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_auto_20151015_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_last_change_date',
            field=models.DateField(default=datetime.date(2015, 10, 15), auto_now=True),
            preserve_default=False,
        ),
    ]
