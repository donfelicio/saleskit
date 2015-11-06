# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicereminder',
            name='invoice_status',
            field=models.CharField(default=1, max_length=255),
        ),
    ]
