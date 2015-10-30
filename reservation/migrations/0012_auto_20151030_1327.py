# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0011_auto_20151030_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuschange',
            options={'ordering': ['res_status_sales_code']},
        ),
        migrations.AddField(
            model_name='statuschange',
            name='res_status_sales',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
