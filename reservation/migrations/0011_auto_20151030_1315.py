# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0010_statuschange'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statuschange',
            old_name='res_intro',
            new_name='change_note',
        ),
        migrations.RenameField(
            model_name='statuschange',
            old_name='res_sales_status_code',
            new_name='res_status_sales_code',
        ),
    ]
