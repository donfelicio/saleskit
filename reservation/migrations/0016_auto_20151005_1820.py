# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_auto_20151005_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statuscodes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_code', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_status_sales',
            field=models.CharField(default=b'Aanvraag ontvangen', max_length=255, choices=[(b'AO', b'Aanvraag ontvangen'), (b'KG', b'Klant gebeld'), (b'BI', b'Bezichtiging ingepland'), (b'OV', b'Offerte verzonden'), (b'ON', b'Offerte nagebeld'), (b'MV', b'Meeting voorbesproken'), (b'AS', b'Aftersales'), (b'DS', b'Deal success'), (b'DF', b'Deal failed')]),
        ),
    ]
