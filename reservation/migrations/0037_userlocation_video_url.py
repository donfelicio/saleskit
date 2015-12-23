# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0036_auto_20151221_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlocation',
            name='video_url',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
