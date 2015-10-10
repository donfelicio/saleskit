# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0021_auto_20151006_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_desc',
            field=models.CharField(default='niets', max_length=255),
            preserve_default=False,
        ),
    ]
