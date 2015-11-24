# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0030_auto_20151124_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_manual_added',
            field=models.CharField(default=b'no', max_length=255),
        ),
    ]
