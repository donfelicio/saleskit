# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0021_auto_20151018_0943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hidereservation',
            old_name='user_key',
            new_name='user_name',
        ),
    ]
