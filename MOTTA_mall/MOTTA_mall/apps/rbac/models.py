from django.contrib.auth.models import AbstractUser
from django.db import models


# 用户
class User(AbstractUser):
    u_phone = models.CharField(max_length=32, verbose_name='电话')
    u_roles = models.ManyToManyField('Role', verbose_name='用户角色')
    u_backup = models.CharField(max_length=32, verbose_name='备用字段')

    def __str__(self):
        return self.username

    class Meta:
        db_table = "tb_user"
        verbose_name = "个人用户信息"
        verbose_name_plural = verbose_name


# 系统管理员 站点管理员 访客
class Role(models.Model):
    r_name = models.CharField(max_length=32, verbose_name='角色名称')
    r_permission = models.ManyToManyField('Permission', verbose_name='权限')
    r_backup = models.CharField(max_length=32, verbose_name='备用字段')

    def __str__(self):
        return self.r_name

    class Meta:


        db_table = "tb_role"
        verbose_name = "角色信息"
        verbose_name_plural = verbose_name


# 权限
class Permission(models.Model):
    p_title = models.CharField(max_length=32, unique=True, verbose_name='标题')
    p_url = models.CharField(max_length=128, unique=True, verbose_name='关联的url')
    p_backup = models.CharField(max_length=32, verbose_name='备用字段')

    def __str__(self):
        return self.p_url

    class Meta:
        db_table = "tb_permission"
        verbose_name = "存储url信息"
        verbose_name_plural = verbose_name

# 用户的登入退出状态记录
class UserStatus(models.Model):
    u_username = models.CharField(max_length=50, verbose_name='用户名称')
    u_grader = models.CharField(max_length=20, verbose_name='用户等级')
    u_outtime = models.CharField(max_length=50, verbose_name='退出时间')
    u_logintime = models.CharField(max_length=50, verbose_name='登入时间')
    u_flg = models.CharField(max_length=10, verbose_name='随机字符串')

    def __str__(self):
        return self.u_username

    class Meta:
        db_table = "tb_UserStatus"
        verbose_name = "存储用户状态信息"
        verbose_name_plural = verbose_name