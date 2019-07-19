from django.db import models
from createdata.models import XmlData
from divices.models import divices


class Warning(models.Model):
    warn_level = models.CharField(max_length=20, verbose_name='告警等级')
    warn_text = models.CharField(max_length=20, verbose_name='告警内容')
    warn_time = models.CharField(max_length=20, verbose_name='告警时间')
    warn_name = models.CharField(max_length=20, verbose_name='告警设备')
    warn_data = models.FloatField(max_length=20, default=None, verbose_name="数据信息值")
    warn_ip = models.CharField(max_length=50, verbose_name="站点ip")
    warn_other = models.CharField(max_length=20, verbose_name="其他")
    unit = models.CharField(max_length=20, verbose_name='单位')
    equip_id = models.ForeignKey(divices, on_delete=models.CASCADE, to_field="divice_ip", verbose_name='告警站点IP')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_warning'
        verbose_name = '告警信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.warn_level


class WarningConfig(models.Model):
    con_address = models.CharField(max_length=20, verbose_name='告警站点地址')
    con_port = models.CharField(max_length=20, verbose_name='告警站点端口')
    con_email = models.EmailField(max_length=20, verbose_name='告警站点邮箱')
    con_password = models.CharField(max_length=20, verbose_name='站点邮箱密码')
    con_phone = models.CharField(max_length=20, verbose_name='站点电话')
    con_ip = models.CharField(max_length=20, verbose_name='站点IP')
    con_other = models.CharField(max_length=20, verbose_name='其他')
    divice = models.OneToOneField(divices, to_field="divice_ip")

    class Meta:
        db_table = 'tb_warningconfig'
        verbose_name = '站点告警配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.con_address
