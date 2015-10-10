# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0036_auto_20151010_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_untouched',
            field=models.CharField(default=b'yes', max_length=255),
        ),
    ]
