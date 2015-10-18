# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_reservation_res_recently_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='res_recently_updated',
        ),
    ]
