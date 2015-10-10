# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0017_auto_20151005_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuscode',
            name='description_short',
            field=models.CharField(default='Aanvraag', max_length=255),
            preserve_default=False,
        ),
    ]
