# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0024_auto_20151018_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='hidereservation',
            name='user_key',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
