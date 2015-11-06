# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_remove_invoicereminder_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicereminder',
            name='invoice_status',
            field=models.IntegerField(default=0),
        ),
    ]
