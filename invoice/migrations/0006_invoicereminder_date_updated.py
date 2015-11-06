# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_invoicereminder_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicereminder',
            name='date_updated',
            field=models.DateField(default=datetime.date(2015, 11, 6), auto_now=True),
            preserve_default=False,
        ),
    ]
