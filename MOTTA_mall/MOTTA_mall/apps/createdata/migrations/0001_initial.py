# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-07-08 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EqModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.IntegerField(default=0, verbose_name='模块ID')),
                ('model_name', models.CharField(max_length=20, verbose_name='模块名称')),
                ('model_data', models.CharField(max_length=50, verbose_name='模块内容')),
                ('model_class', models.CharField(max_length=20, verbose_name='模块分类')),
                ('model_ip', models.CharField(max_length=50, verbose_name='ip字段')),
                ('model_other', models.CharField(max_length=50, verbose_name='其他')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
            ],
            options={
                'verbose_name': '环境模块',
                'verbose_name_plural': '环境模块',
                'db_table': 'tb_eqmodel',
            },
        ),
        migrations.CreateModel(
            name='EquipmentData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment', models.CharField(max_length=50, verbose_name='设备')),
                ('equipment_name', models.CharField(max_length=50, verbose_name='设备名称')),
                ('equipment_text', models.CharField(max_length=50, verbose_name='内容信息')),
                ('equipment_unit', models.CharField(max_length=20, verbose_name='单位')),
                ('equipment_other', models.CharField(max_length=50, verbose_name='其他')),
                ('equipment_ip', models.CharField(max_length=50, verbose_name='ip字段')),
            ],
            options={
                'verbose_name': '设备详细信息',
                'verbose_name_plural': '设备详细信息',
                'db_table': 'tb_EquipmentData',
            },
        ),
        migrations.CreateModel(
            name='XmlData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipid', models.CharField(max_length=20, verbose_name='设备ID')),
                ('sigid', models.CharField(max_length=20, verbose_name='信号ID')),
                ('reg_addr', models.CharField(max_length=20, verbose_name='寄存器地址')),
                ('name', models.CharField(max_length=50, verbose_name='信号名称')),
                ('float_data', models.FloatField(verbose_name='获取数据')),
                ('data_time', models.CharField(max_length=50, verbose_name='时间戳')),
                ('divice_ip', models.CharField(max_length=50, verbose_name='IP地址')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
            ],
            options={
                'verbose_name': '监控设备详细信息',
                'verbose_name_plural': '监控设备详细信息',
                'db_table': 'tb_xmldata',
            },
        ),
    ]
