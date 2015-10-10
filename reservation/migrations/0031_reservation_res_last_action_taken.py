# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0030_filteroption_filter_short'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_last_action_taken',
            field=models.DateField(null=True),
        ),
    ]
