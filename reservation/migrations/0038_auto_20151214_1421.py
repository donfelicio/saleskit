# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0037_reservation_res_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_company',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='res_desc',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='res_user',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_status',
            field=models.CharField(default=b'1', max_length=255, choices=[(b'3', b'cancelled'), (b'1', b'attention required'), (b'2', b'final')]),
        ),
    ]
