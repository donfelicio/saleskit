# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0037_userlocation_video_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_id', models.CharField(max_length=255, null=True)),
                ('location_name', models.CharField(max_length=255, null=True)),
                ('video_url', models.CharField(default=b'', max_length=255)),
                ('user', models.ForeignKey(to='reservation.Userprofile')),
            ],
        ),
    ]
