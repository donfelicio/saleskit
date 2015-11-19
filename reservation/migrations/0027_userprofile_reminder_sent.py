# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0026_remove_reservationfilter_res_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='reminder_sent',
            field=models.DateField(null=True),
        ),
    ]
