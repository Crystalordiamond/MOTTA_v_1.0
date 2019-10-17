# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-16 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_title', models.CharField(max_length=32, unique=True, verbose_name='标题')),
                ('p_url', models.CharField(max_length=128, unique=True, verbose_name='关联的url')),
                ('p_backup', models.CharField(max_length=32, verbose_name='备用字段')),
            ],
            options={
                'verbose_name': '存储url信息',
                'verbose_name_plural': '存储url信息',
                'db_table': 'tb_permission',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_name', models.CharField(max_length=32, verbose_name='角色名称')),
                ('r_backup', models.CharField(max_length=32, verbose_name='备用字段')),
                ('r_permission', models.ManyToManyField(to='rbac.Permission', verbose_name='权限')),
            ],
            options={
                'verbose_name': '角色信息',
                'verbose_name_plural': '角色信息',
                'db_table': 'tb_role',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_account', models.CharField(max_length=32, verbose_name='用户名')),
                ('u_password', models.CharField(max_length=32, verbose_name='密码')),
                ('u_email', models.CharField(max_length=32, verbose_name='邮箱')),
                ('u_phone', models.CharField(max_length=32, verbose_name='电话')),
                ('u_backup', models.CharField(max_length=32, verbose_name='备用字段')),
                ('u_roles', models.ManyToManyField(to='rbac.Role', verbose_name='用户角色')),
            ],
            options={
                'verbose_name': '个人用户信息',
                'verbose_name_plural': '个人用户信息',
                'db_table': 'tb_user',
            },
        ),
    ]