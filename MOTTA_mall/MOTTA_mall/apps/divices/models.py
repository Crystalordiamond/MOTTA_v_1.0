from django.db import models
from rbac.models import User


# 1.站点信息
class divices(models.Model):
    divice_ip = models.CharField(max_length=50, verbose_name='ip地址', unique=True)
    divice_location = models.EmailField(max_length=50, null=True, verbose_name='ip地址')
    user_id = models.ManyToManyField(User, verbose_name='站点关联的用户')
    divice_site = models.EmailField(max_length=50, null=True, verbose_name='MDC1')
    divice_communication = models.CharField(max_length=50, null=True, verbose_name="协议类型")
    divice_type = models.CharField(max_length=50, null=True, verbose_name="机器型号")
    divice_serial = models.CharField(max_length=50, null=True, verbose_name='机器序列号')

    class Meta:
        db_table = 'tb_divices'
        verbose_name = '站点信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.divice_location


# 2.站点的邮件告警配置
class WarningConfig(models.Model):
    con_server = models.CharField(max_length=20, verbose_name='告警服务器')
    con_port = models.CharField(max_length=20, verbose_name='告警站点端口')
    con_method = models.CharField(max_length=20, verbose_name='告警站点端口')
    con_account = models.EmailField(max_length=50, default="null") #发邮件的邮箱
    con_password = models.CharField(max_length=20) # 邮箱密码
    con_phone = models.CharField(max_length=20, verbose_name='站点电话')
    con_ip = models.CharField(max_length=20, verbose_name='站点IP')
    con_other = models.CharField(max_length=20, verbose_name='其他')

    class Meta:
        db_table = 'tb_warningconfig'
        verbose_name = '站点告警配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.con_server


# 3.站点摄像头配置
class Cameras(models.Model):
    cam_site = models.CharField(max_length=20, null=True, verbose_name='MDC1')
    cam_location = models.CharField(max_length=20, null=True, verbose_name='站点位置')
    cam_address = models.CharField(max_length=20, verbose_name='摄像头IP')
    cam_ip = models.CharField(max_length=20, verbose_name='站点IP')
    cam_other = models.CharField(max_length=20, null=True, verbose_name='其他')

    class Meta:
        db_table = 'tb_Cameras'
        verbose_name = '站点摄像头配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cam_address


# 4.经纬度坐标点
class coordinate(models.Model):
    coordinate_ip = models.CharField(max_length=50, verbose_name='ip地址', unique=True)
    coordinate_location = models.CharField(max_length=50, null=True, verbose_name='站点名称') #
    coordinate_site = models.CharField(max_length=50, null=True, verbose_name='MDC1')
    coordinate_status = models.CharField(max_length=50, null=True, verbose_name="告警状态")
    coordinate_A = models.FloatField(max_length=30, verbose_name='坐标点A')
    coordinate_B = models.FloatField(max_length=30, verbose_name='坐标点B')
    coordinate_address = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = 'tb_coordinate'
        verbose_name = '坐标点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.coordinate_ip
