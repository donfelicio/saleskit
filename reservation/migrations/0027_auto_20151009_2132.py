# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0026_auto_20151009_1754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ['res_date']},
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_status',
            field=models.CharField(default=b'1', max_length=255, choices=[(b'3', b'cancelled'), (b'1', b'attention required'), (b'2', b'final')]),
        ),
    ]
