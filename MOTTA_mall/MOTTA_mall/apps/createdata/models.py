from django.db import models
from divices.models import divices


class XmlData(models.Model):
    equipid = models.CharField(max_length=20, verbose_name="设备ID")
    sigid = models.CharField(max_length=20, verbose_name="信号ID")
    reg_addr = models.CharField(max_length=20, verbose_name="寄存器地址")
    name = models.CharField(max_length=50, verbose_name="信号名称")
    float_data = models.FloatField(verbose_name="获取数据")
    # data_time = models.DateTimeField(verbose_name="时间戳")  # Django 项目中的自动获取时间 是需要用户来操作保存的。项目外的py文件保存数据库需要手动添加，不然回报错
    data_time = models.CharField(max_length=50, verbose_name="时间戳")
    divice_ip = models.CharField(max_length=50, verbose_name="IP地址")
    # 先注销关联性
    # divice_id = models.ForeignKey(divices, on_delete=models.CASCADE, verbose_name='站点ID')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = "tb_xmldata"
        verbose_name = "监控设备详细信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.equipid


# 用于展示历史数据
class EquipmentData(models.Model):
    equipment = models.CharField(max_length=50, verbose_name="设备")
    equipment_name = models.CharField(max_length=50, verbose_name="设备名称")
    equipment_text = models.CharField(max_length=50, verbose_name="内容信息")
    equipment_unit = models.CharField(max_length=20, verbose_name="单位")
    equipment_folat = models.FloatField(default=False, verbose_name="信息值")
    equipment_time = models.CharField(default=False, max_length=50, verbose_name="时间")
    equipment_other = models.CharField(max_length=50, verbose_name="其他")
    equipment_ip = models.CharField(max_length=50, verbose_name='ip字段')
    divices = models.ForeignKey(divices, on_delete=models.CASCADE, to_field="divice_ip", verbose_name="关联IP")

    # divices = models.ForeignKey(divices, on_delete=models.CASCADE, verbose_name="关联站点的id")

    class Meta:
        db_table = "tb_EquipmentData"
        verbose_name = "设备详细信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.equipment


# 环境模块
class EqModel(models.Model):
    model_id = models.IntegerField(default=0, verbose_name='模块ID')
    model_name = models.CharField(max_length=20, verbose_name='模块名称')
    model_data = models.CharField(max_length=50, verbose_name='模块内容')
    model_class = models.CharField(max_length=20, verbose_name='模块分类')
    model_ip = models.CharField(max_length=50, verbose_name='ip字段')
    model_other = models.CharField(max_length=50, verbose_name='其他')
    equip_id = models.ForeignKey(divices, on_delete=models.CASCADE, to_field="divice_ip", verbose_name='关联设备')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_eqmodel'
        verbose_name = '环境模块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.model_name


# 站点配置模块
class AddressConfig(models.Model):
    server_address = models.CharField(max_length=50, verbose_name='服务器地址')
    port_config = models.IntegerField(default=False, verbose_name='端口配置')
    send_mail = models.CharField(max_length=50, verbose_name='发件箱')
    password = models.CharField(max_length=20, verbose_name='密码')
    COM_phone = models.CharField(max_length=50, verbose_name='电话端口号')
    other_config = models.CharField(max_length=50, verbose_name='其他设置')
    divice_ip = models.CharField(default=False, max_length=50, verbose_name='关联ip字段')

    class Meta:
        db_table = 'tb_addressconfig'
        verbose_name = '站点配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.server_address
