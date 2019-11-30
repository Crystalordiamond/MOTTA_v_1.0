from django.db import models
from divices.models import divices


# 告警实时展示给前端的数据表
class AlarmContent(models.Model):
    EquipTemplateId = models.CharField(max_length=25, verbose_name='EquipTemplateId')
    site = models.CharField(max_length=25, verbose_name='告警的站点')
    alarm = models.CharField(max_length=150, verbose_name='告警的名称')
    alarm_text = models.CharField(max_length=50, verbose_name='告警的内容')
    equipment = models.CharField(max_length=25, verbose_name='告警的设备')
    level = models.CharField(max_length=25, verbose_name='告警等级')
    manage = models.CharField(max_length=25, verbose_name='点关联的用户')
    lssue_time = models.CharField(max_length=25, verbose_name='告警时间')
    alarm_id = models.CharField(max_length=25, verbose_name='告警的ID')
    alarm_ip = models.CharField(max_length=25, verbose_name='告警的IP')
    alarm_flag = models.CharField(max_length=25, default='-', verbose_name='告警标识')

    class Meta:
        db_table = 'tb_AlarmContent'
        verbose_name = '实时告警列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.alarm_text


# 1.用于展示历史告警信息
class Warning(models.Model):
    warn_site = models.CharField(max_length=20, verbose_name='告警站点')
    warn_equipment = models.CharField(max_length=20, verbose_name='告警设备')
    warn_parameter = models.CharField(max_length=20, verbose_name='告警参数')
    warn_alarm = models.CharField(max_length=120, verbose_name='告警内容')
    warn_value = models.CharField(max_length=20, verbose_name='告警值')
    warn_unit = models.CharField(max_length=10, default="-", null=False, verbose_name='告警单位')
    warn_level = models.CharField(max_length=20, verbose_name='告警等级')
    warn_time = models.CharField(max_length=20, verbose_name='告警时间')
    warn_ip = models.CharField(max_length=50, verbose_name="站点ip")
    warn_other = models.CharField(max_length=20, verbose_name="其他")

    # equip_id = models.ForeignKey(divices, on_delete=models.CASCADE, to_field="divice_ip", verbose_name='告警站点IP')
    # is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_warning'
        verbose_name = '告警信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.warn_level


# 用于展示历史数据(实数数据的表 数据量太多 查询无法分割)
class HistoryData(models.Model):
    equipment_site = models.CharField(max_length=20, verbose_name='MDC')
    equipment_equipment = models.CharField(max_length=20, verbose_name='温湿度')
    equipment_parameter = models.CharField(max_length=20, verbose_name='参数')
    equipment_value = models.CharField(max_length=20, verbose_name='值')
    equipment_unit = models.CharField(max_length=20, default="-", null=False, verbose_name='单位')
    equipment_time = models.CharField(max_length=20, verbose_name='时间')
    equipment_ip = models.CharField(max_length=50, verbose_name="站点ip")
    equipment_other = models.CharField(max_length=50, verbose_name="其他")

    class Meta:
        db_table = "tb_historydata"
        verbose_name = "设备详细信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.equipment_site
