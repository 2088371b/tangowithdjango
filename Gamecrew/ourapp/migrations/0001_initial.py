# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gameID', models.IntegerField(default=0, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('server', models.CharField(default=b'World', max_length=128)),
                ('platform', models.CharField(default=b'PC', max_length=128)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(to='ourapp.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('game', models.ForeignKey(to='ourapp.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
