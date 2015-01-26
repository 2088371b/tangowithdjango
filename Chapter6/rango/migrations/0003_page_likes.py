# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20150124_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
