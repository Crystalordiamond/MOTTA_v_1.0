# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-28 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='divices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('divice_ip', models.CharField(max_length=50, unique=True, verbose_name='ip地址')),
                ('divice_name', models.EmailField(max_length=50, verbose_name='站点名称')),
                ('divice_email', models.EmailField(max_length=50, verbose_name='站点邮箱')),
                ('divice_phone', models.CharField(max_length=50, verbose_name='站点电话')),
                ('divice_other', models.CharField(max_length=50, verbose_name='其他')),
                ('is_delete', models.IntegerField(default=False, verbose_name='逻辑删除')),
            ],
            options={
                'verbose_name': '站点信息',
                'verbose_name_plural': '站点信息',
                'db_table': 'tb_divices',
            },
        ),
    ]
