# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-05 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20161202_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='hostname',
            field=models.CharField(max_length=32, unique=True, verbose_name='\u4e3b\u673a\u540d'),
        ),
        migrations.AlterField(
            model_name='host',
            name='innerip',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='outerip',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]