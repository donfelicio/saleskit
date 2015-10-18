# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_userlocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_key', models.CharField(max_length=255, null=True)),
                ('active_location', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userlocation',
            name='location_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
