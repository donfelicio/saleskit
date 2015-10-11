# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0038_auto_20151011_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_last_action_taken',
            field=models.DateField(auto_now=True),
        ),
    ]
