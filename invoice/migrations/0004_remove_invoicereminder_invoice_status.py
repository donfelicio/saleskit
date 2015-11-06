# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_auto_20151105_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicereminder',
            name='invoice_status',
        ),
    ]
