# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0038_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='user',
        ),
    ]
