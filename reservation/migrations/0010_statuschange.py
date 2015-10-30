# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0009_auto_20151028_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statuschange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('change_date', models.DateTimeField(auto_now=True, null=True)),
                ('res_id', models.CharField(max_length=255, null=True)),
                ('res_sales_status_code', models.CharField(max_length=255, null=True)),
                ('res_intro', models.TextField(default=b'', null=True)),
            ],
        ),
    ]
