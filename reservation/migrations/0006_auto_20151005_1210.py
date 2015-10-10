# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_auto_20151005_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='res_date',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_date_created',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_user',
            field=models.CharField(max_length=255),
        ),
    ]
