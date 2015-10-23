# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_auto_20151022_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loginlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('last_login', models.DateField(auto_now=True, null=True)),
            ],
        ),
    ]
