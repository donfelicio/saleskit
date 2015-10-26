# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20151023_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='loc_updated',
            field=models.CharField(default=b'not', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='res_updated',
            field=models.CharField(default=b'not', max_length=255),
        ),
    ]
