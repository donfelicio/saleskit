# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0018_auto_20151016_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='res_updated',
            field=models.CharField(default=b'no', max_length=255),
        ),
    ]
