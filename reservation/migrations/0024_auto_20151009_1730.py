# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0023_reservation_res_total_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_company',
            field=models.CharField(default='nobody', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_user',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
