# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0009_delete_filteroption'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_last_step_before_cancel',
            field=models.CharField(default=b'9', max_length=255),
        ),
    ]
