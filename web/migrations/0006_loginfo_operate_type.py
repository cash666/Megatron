# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-12 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_remove_loginfo_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginfo',
            name='operate_type',
            field=models.CharField(default='\u6279\u91cf\u64cd\u4f5c', max_length=32, verbose_name='\u64cd\u4f5c\u7c7b\u578b'),
            preserve_default=False,
        ),
    ]
