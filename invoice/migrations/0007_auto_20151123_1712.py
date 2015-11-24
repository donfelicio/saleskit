# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_invoicereminder_date_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoicereminder',
            options={'ordering': ['-date_updated']},
        ),
    ]
