# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_auto_20151014_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='filteroption',
            name='filter_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
