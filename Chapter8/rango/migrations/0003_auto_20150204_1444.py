# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_page_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='slug',
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
    ]
