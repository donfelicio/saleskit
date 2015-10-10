# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0028_filteroptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filteroption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter_name', models.CharField(max_length=255, null=True)),
                ('filter_desc', models.CharField(max_length=255, null=True)),
                ('filter_status', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Filteroptions',
        ),
    ]
