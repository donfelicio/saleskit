# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0027_auto_20151009_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filteroptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter_code', models.CharField(unique=True, max_length=255)),
                ('filter_name', models.CharField(max_length=255, null=True)),
                ('filter_desc', models.CharField(max_length=255, null=True)),
                ('filter_status', models.CharField(max_length=255)),
            ],
        ),
    ]
