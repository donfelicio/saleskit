# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoicereminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_id', models.CharField(max_length=255, null=True)),
                ('invoice_status', models.CharField(max_length=255, null=True)),
                ('sent_stage', models.CharField(default=b'no', max_length=255)),
            ],
        ),
    ]
