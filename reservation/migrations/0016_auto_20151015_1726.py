# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_remove_reservation_res_last_action_taken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hidereservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('res_id', models.CharField(max_length=255, null=True)),
                ('user_key', models.CharField(max_length=255, null=True)),
                ('hide_days', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='res_untouched',
        ),
    ]
