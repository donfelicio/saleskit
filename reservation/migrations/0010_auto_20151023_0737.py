# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0009_loginlog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loginlog',
            old_name='last_login',
            new_name='login_date',
        ),
    ]
