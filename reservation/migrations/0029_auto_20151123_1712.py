# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0028_refreshlog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loginlog',
            options={'ordering': ['-login_date']},
        ),
        migrations.AlterModelOptions(
            name='refreshlog',
            options={'ordering': ['-login_date']},
        ),
    ]
