# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0024_auto_20151009_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_location_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
