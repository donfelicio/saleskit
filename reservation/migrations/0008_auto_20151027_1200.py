# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_reservation_res_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginlog',
            name='login_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
