# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_auto_20151005_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_status_sales',
            field=models.CharField(default=b'Aanvraag ontvangen', max_length=255, choices=[(b'Aanvraag ontvangen', b'Aanvraag ontvangen'), (b'Klant gebeld', b'Klant gebeld'), (b'Bezichtiging ingepland', b'Bezichtiging ingepland'), (b'Offerte verzonden', b'Offerte verzonden'), (b'Offerte nagebeld', b'Offerte nagebeld'), (b'Meeting voorbesproken', b'Meeting voorbesproken'), (b'Aftersales', b'Aftersales'), (b'Deal success', b'Deal success'), (b'Deal failed', b'Deal failed')]),
        ),
    ]
