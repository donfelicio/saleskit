# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loginlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('login_date', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('res_id', models.CharField(unique=True, max_length=255)),
                ('res_user', models.CharField(max_length=255, null=True)),
                ('res_location_id', models.CharField(max_length=255, null=True)),
                ('res_company', models.CharField(max_length=255)),
                ('res_desc', models.CharField(max_length=255)),
                ('res_date_created', models.DateField()),
                ('res_date', models.DateField()),
                ('res_status', models.CharField(default=b'1', max_length=255, choices=[(b'3', b'cancelled'), (b'1', b'attention required'), (b'2', b'final')])),
                ('res_status_sales', models.CharField(default=b'1', max_length=255, choices=[(b'1', b'Request received'), (b'2', b'Called customer'), (b'3', b'Location tour planned'), (b'4', b'Sent offer'), (b'5', b'Called about offer'), (b'6', b'Prepared meeting'), (b'7', b'Aftersales'), (b'8', b'Deal success'), (b'9', b'Deal failed')])),
                ('res_total_seats', models.CharField(max_length=255, null=True)),
                ('res_prev_status', models.CharField(default=b'9', max_length=255, choices=[(b'1', b'Request received'), (b'2', b'Called customer'), (b'3', b'Location tour planned'), (b'4', b'Sent offer'), (b'5', b'Called about offer'), (b'6', b'Prepared meeting'), (b'7', b'Aftersales'), (b'8', b'Deal success'), (b'9', b'Deal failed')])),
                ('res_last_change_by', models.CharField(max_length=255, null=True)),
                ('res_last_change_date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['res_date', 'res_id'],
            },
        ),
        migrations.CreateModel(
            name='Reservationfilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('res_id', models.CharField(max_length=255, null=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('hide_days', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Statuscode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_code', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('description_short', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Userlocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_id', models.CharField(max_length=255, null=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('location_name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('user_key', models.CharField(max_length=255, null=True)),
                ('active_location', models.CharField(default=False, max_length=255)),
                ('last_login', models.DateField(auto_now=True, null=True)),
                ('res_updated', models.CharField(default=b'no', max_length=255)),
                ('loc_updated', models.CharField(default=b'no', max_length=255)),
            ],
        ),
    ]
