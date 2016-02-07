# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0039_auto_20151228_2033'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
    ]
