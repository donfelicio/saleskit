# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0011_auto_20151015_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_last_change_by',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
