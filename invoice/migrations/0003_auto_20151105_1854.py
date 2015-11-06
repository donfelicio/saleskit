# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20151105_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicereminder',
            name='invoice_status',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
