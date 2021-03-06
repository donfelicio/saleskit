# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20151023_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_prev_status',
            field=models.CharField(default=b'9', max_length=255, choices=[(b'1', b'Request received'), (b'2', b'Called customer'), (b'3', b'Location tour planned'), (b'4', b'Sent offer'), (b'5', b'Called about offer'), (b'6', b'Prepared meeting'), (b'7', b'Aftersales'), (b'8', b'Deal success'), (b'9', b'Deal failed')]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_status_sales',
            field=models.CharField(default=b'1', max_length=255, choices=[(b'1', b'Request received'), (b'2', b'Called customer'), (b'3', b'Location tour planned'), (b'4', b'Sent offer'), (b'5', b'Called about offer'), (b'6', b'Prepared meeting'), (b'7', b'Aftersales'), (b'8', b'Deal success'), (b'9', b'Deal failed')]),
        ),
    ]
