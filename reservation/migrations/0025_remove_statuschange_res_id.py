# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0024_statuschange_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statuschange',
            name='res_id',
        ),
    ]
