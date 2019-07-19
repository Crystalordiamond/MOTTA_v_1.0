# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-07-11 09:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('createdata', '0004_addressconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressconfig',
            name='divices',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='divices.divices', to_field='divice_ip', verbose_name='关联站点'),
        ),
    ]
