# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_auto_20151026_1248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuscode',
            options={'ordering': ['status_code']},
        ),
    ]
