# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0029_auto_20151010_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='filteroption',
            name='filter_short',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
