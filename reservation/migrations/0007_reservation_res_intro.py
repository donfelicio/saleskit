# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_auto_20151026_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_intro',
            field=models.TextField(null=True),
        ),
    ]
