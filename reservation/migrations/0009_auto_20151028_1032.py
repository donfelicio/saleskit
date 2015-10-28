# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_auto_20151027_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_intro',
            field=models.TextField(default=b'', null=True),
        ),
    ]
