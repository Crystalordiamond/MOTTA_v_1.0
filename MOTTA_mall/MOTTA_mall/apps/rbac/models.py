from django.db import models


# 用户
class User(models.Model):
    u_account = models.CharField(max_length=32, verbose_name='用户名')
    u_password = models.CharField(max_length=32, verbose_name='密码')
    u_email = models.CharField(max_length=32, verbose_name='邮箱')
    u_phone = models.CharField(max_length=32, verbose_name='电话')
    u_roles = models.ManyToManyField('Role', verbose_name='用户角色')
    u_backup = models.CharField(max_length=32, verbose_name='备用字段')

    def __str__(self):
        return self.u_account

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
