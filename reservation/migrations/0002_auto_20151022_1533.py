# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlocation',
            name='user_key',
        ),
        migrations.AddField(
            model_name='userlocation',
            name='user_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
