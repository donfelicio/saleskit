# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_auto_20151014_1242'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Filteroption',
        ),
    ]
