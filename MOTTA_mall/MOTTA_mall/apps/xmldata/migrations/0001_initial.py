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
            name='equipments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EquipId', models.IntegerField(max_length=50)),
                ('EquipTemplateId', models.CharField(max_length=50)),
                ('EquipmentName', models.CharField(max_length=50)),
                ('EquipAddress', models.CharField(max_length=50)),
                ('LibName', models.CharField(max_length=50)),
                ('Equipment_ip', models.CharField(max_length=50)),
                ('Equipment_time', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '设备中间表',
                'verbose_name_plural': '设备中间表',
                'db_table': 'tb_equipments',
            },
        ),
        migrations.CreateModel(
            name='equiptemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SignalId', models.CharField(max_length=50)),
                ('SignalName', models.CharField(max_length=150)),
                ('EquipTemplateId', models.CharField(max_length=50)),
                ('EquipTemplateName', models.CharField(max_length=50)),
                ('StateValue', models.CharField(blank=True, max_length=50, null=True)),
                ('Meaning', models.CharField(blank=True, max_length=50, null=True)),
                ('equiptemplate_ip', models.CharField(max_length=50)),
                ('equiptemplate_time', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '状态信息表',
                'verbose_name_plural': '状态信息表',
                'db_table': 'tb_equiptemplate',
            },
        ),
        migrations.CreateModel(
            name='port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PortId', models.IntegerField(max_length=50)),
                ('PortNo', models.CharField(max_length=50)),
                ('PortType', models.CharField(max_length=50)),
                ('PortSetting', models.CharField(max_length=50)),
                ('PortLibName', models.CharField(blank=True, max_length=50, null=True)),
                ('Description', models.CharField(blank=True, max_length=50, null=True)),
                ('port_ip', models.CharField(max_length=50)),
                ('port_time', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '端口信息表',
                'verbose_name_plural': '端口信息表',
                'db_table': 'tb_port',
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
                'verbose_name': '实时信息表',
                'verbose_name_plural': '实时信息表',
                'db_table': 'tb_xmldata',
            },
        ),
    ]