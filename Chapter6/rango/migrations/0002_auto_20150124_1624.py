# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='category',
            name='views',
        ),
        migrations.RemoveField(
            model_name='page',
            name='likes',
        ),
        migrations.AlterField(
            model_name='page',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
