# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0016_auto_20151005_1820'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Statuscodes',
            new_name='Statuscode',
        ),
    ]
