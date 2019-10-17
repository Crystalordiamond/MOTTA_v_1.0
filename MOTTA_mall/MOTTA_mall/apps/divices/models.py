from django.db import models
from rbac.models import User


# 站点
class divices(models.Model):
    divice_ip = models.CharField(max_length=50, verbose_name='ip地址', unique=True)
    divice_location = models.EmailField(max_length=50, verbose_name='站点名称')
    user_id = models.ManyToManyField(User, verbose_name='站点关联的用户')
    divice_site = models.EmailField(max_length=50, verbose_name='MDC1')
    divice_communication = models.CharField(max_length=50, verbose_name="协议类型")
    divice_type = models.CharField(max_length=50, verbose_name="机器型号")
    divice_serial = models.CharField(max_length=50, verbose_name='机器序列号')

    class Meta:
        db_table = 'tb_divices'
        verbose_name = '站点信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.divice_location
