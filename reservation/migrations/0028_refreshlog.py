# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0027_userprofile_reminder_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refreshlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('login_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
