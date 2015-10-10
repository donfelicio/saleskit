# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_auto_20151005_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_status_sales',
            field=models.CharField(default=1, max_length=255, choices=[(1, b'Aanvraag ontvangen'), (2, b'Klant gebeld'), (3, b'Bezichtiging ingepland'), (4, b'Offerte verzonden'), (5, b'Offerte nagebeld'), (6, b'Meeting voorbesproken'), (7, b'Aftersales'), (8, b'Deal success'), (9, b'Deal failed')]),
        ),
    ]
