# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-07-10 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createdata', '0002_auto_20190708_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentdata',
            name='equipment_folat',
            field=models.FloatField(default=False, verbose_name='信息值'),
        ),
        migrations.AddField(
            model_name='equipmentdata',
            name='equipment_time',
            field=models.CharField(default=False, max_length=50, verbose_name='时间'),
        ),
    ]
