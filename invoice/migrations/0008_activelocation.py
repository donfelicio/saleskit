# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_auto_20151123_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activelocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_id', models.IntegerField(default=0)),
                ('profile_key', models.CharField(default=None, max_length=255)),
            ],
        ),
    ]
