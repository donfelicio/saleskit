# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_auto_20151005_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_status',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
