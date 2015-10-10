# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0019_auto_20151005_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_id',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
