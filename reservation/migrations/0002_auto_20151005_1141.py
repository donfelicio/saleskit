# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_date',
            field=models.CharField(default=datetime.datetime(2015, 10, 5, 11, 41, 14, 736721, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='res_date_created',
            field=models.CharField(default=datetime.datetime(2015, 10, 5, 11, 41, 25, 104208, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='res_user',
            field=models.CharField(default=datetime.datetime(2015, 10, 5, 11, 41, 48, 92035, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
    ]
