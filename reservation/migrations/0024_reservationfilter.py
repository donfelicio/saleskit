# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0023_delete_reservationfilter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservationfilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('res_id', models.CharField(max_length=255, null=True)),
                ('location_id', models.CharField(max_length=255, null=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('hide_days', models.DateField(null=True)),
                ('hide_hour', models.CharField(max_length=255, null=True)),
                ('hide_minute', models.CharField(max_length=255, null=True)),
                ('reservation', models.ForeignKey(to='reservation.Reservation')),
            ],
        ),
    ]
