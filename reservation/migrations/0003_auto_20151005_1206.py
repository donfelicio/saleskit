# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20151005_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_status',
            field=models.CharField(default=None, max_length=1),
        ),
        migrations.AddField(
            model_name='reservation',
            name='res_status_sales',
            field=models.CharField(default=1, max_length=1, choices=[(1, b'aanvraag ontvangen'), (2, b'klant gebeld')]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_date',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_date_created',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_id',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_user',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
