from django.db import models


# 1、map数据表
class XmlData(models.Model):
    equipid = models.CharField(max_length=20, verbose_name="设备ID")
    sigid = models.CharField(max_length=20, verbose_name="信号ID")
    reg_addr = models.CharField(max_length=20, verbose_name="寄存器地址")
    name = models.CharField(max_length=50, verbose_name="信号名称")
    float_data = models.FloatField(verbose_name="获取数据")
    # data_time = models.DateTimeField(verbose_name="时间戳")  # Django 项目中的自动获取时间 是需要用户来操作保存的。项目外的py文件保存数据库需要手动添加，不然回报错
    data_time = models.CharField(max_length=50, verbose_name="时间戳")
    divice_ip = models.CharField(max_length=50, verbose_name="IP地址")
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    # 先注销关联性
    # divice_id = models.ForeignKey(divices, on_delete=models.CASCADE, verbose_name='站点ID')

    class Meta:
        db_table = "tb_xmldata"
        verbose_name = "实时信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 2、 设备中间表
class equipments(models.Model):
    EquipId = models.CharField(max_length=50)
    EquipTemplateId = models.CharField(max_length=50)
    EquipmentName = models.CharField(max_length=50)
    EquipAddress = models.CharField(max_length=50)
    LibName = models.CharField(max_length=50)
    Equipment_ip = models.CharField(max_length=50)
    Equipment_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_equipments'
        verbose_name = "设备中间表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.LibName


# 3、状态信息表
class equiptemplate(models.Model):
    SignalId = models.CharField(max_length=50)
    SignalName = models.CharField(max_length=150)
    EquipTemplateId = models.CharField(max_length=50)
    EquipTemplateName = models.CharField(max_length=50)
    StateValue = models.CharField(max_length=50, null=True, blank=True)
    Meaning = models.CharField(max_length=50, null=True, blank=True)
    equiptemplate_ip = models.CharField(max_length=50)
    equiptemplate_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_equiptemplate'
        verbose_name = "状态信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.EquipTemplateName


# 端口表
class port(models.Model):
    PortId = models.CharField(max_length=50)
    PortNo = models.CharField(max_length=50)
    PortType = models.CharField(max_length=50)
    PortSetting = models.CharField(max_length=50)
    PortLibName = models.CharField(max_length=50, null=True, blank=True)
    Description = models.CharField(max_length=50, null=True, blank=True)
    port_ip = models.CharField(max_length=50)
    port_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_port'
        verbose_name = "端口信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.PortId
