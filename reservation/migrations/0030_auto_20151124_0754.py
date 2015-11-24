# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0029_auto_20151123_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remindlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('log_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['-log_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='refreshlog',
            options={'ordering': ['-log_date']},
        ),
        migrations.RenameField(
            model_name='refreshlog',
            old_name='login_date',
            new_name='log_date',
        ),
    ]
