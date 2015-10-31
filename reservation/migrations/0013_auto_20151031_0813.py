# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0012_auto_20151030_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuschange',
            options={'ordering': ['-res_status_sales_code']},
        ),
    ]
