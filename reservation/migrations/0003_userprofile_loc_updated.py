# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20151022_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='loc_updated',
            field=models.CharField(default=b'no', max_length=255),
        ),
    ]
