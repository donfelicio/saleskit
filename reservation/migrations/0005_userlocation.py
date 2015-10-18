# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_remove_reservation_res_recently_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userlocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_id', models.CharField(max_length=255, null=True)),
                ('user_key', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
