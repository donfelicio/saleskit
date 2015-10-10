# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0018_statuscode_description_short'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_status_sales',
            field=models.CharField(default=b'1', max_length=255, choices=[(b'1', b'Aanvraag ontvangen'), (b'2', b'Klant gebeld'), (b'3', b'Bezichtiging ingepland'), (b'4', b'Offerte verzonden'), (b'5', b'Offerte nagebeld'), (b'6', b'Meeting voorbesproken'), (b'7', b'Aftersales'), (b'8', b'Deal success'), (b'9', b'Deal failed')]),
        ),
    ]
