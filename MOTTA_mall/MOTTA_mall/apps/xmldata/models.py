from django.db import models


# map数据表
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


# 1、端口表<Ports>
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


# 2、 设备中间表<Equipments>
class equipments(models.Model):
    EquipId = models.CharField(max_length=50)
    EquipTemplateId = models.CharField(max_length=50)
    EquipmentName = models.CharField(max_length=50)
    PortId = models.CharField(null=True,max_length=25)
    EquipAddress = models.CharField(max_length=25)
    LibName = models.CharField(max_length=50)
    Equipment_ip = models.CharField(max_length=50)
    Equipment_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_equipments'
        verbose_name = "设备中间表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.LibName


# 3、 <LogActions>
class logactions(models.Model):
    LogActionId = models.CharField(max_length=50)
    ActionName = models.CharField(max_length=50)
    TriggerType = models.CharField(max_length=50)
    ActionId = models.CharField(max_length=25)
    EquipmentId = models.CharField(max_length=25)
    ActionValue = models.CharField(max_length=50)
    logactions_ip = models.CharField(max_length=50)
    logactions_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_logactions'
        verbose_name = "设备第三张表<LogActions>"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ActionName


#  1、<Signals>状态信息表
class Signals(models.Model):
    EquipTemplateId = models.CharField(max_length=50)
    EquipTemplateName = models.CharField(max_length=50)
    EquipTemplateType = models.CharField(max_length=50)
    LibName = models.CharField(max_length=50)

    SignalId = models.CharField(max_length=50)
    SignalName = models.CharField(max_length=150)
    SignalBaseId = models.CharField(max_length=150)
    SignalType = models.CharField(max_length=150)

    StateValue = models.CharField(max_length=50, null=True, blank=True)
    Meaning = models.CharField(max_length=50, null=True, blank=True)

    Signals_ip = models.CharField(max_length=50)
    Signals_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_Signals'
        verbose_name = "状态信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.EquipTemplateName


#  2、<Events>状态信息表
class Events(models.Model):
    EquipTemplateId = models.CharField(max_length=50)
    EquipTemplateName = models.CharField(max_length=50)
    EquipTemplateType = models.CharField(max_length=50)
    LibName = models.CharField(max_length=50)

    EventId = models.CharField(max_length=50)
    EventName = models.CharField(max_length=150)
    ConditionId = models.CharField(max_length=50)
    Meaning = models.CharField(max_length=50)
    EventSeverity = models.CharField(max_length=50)

    Events_ip = models.CharField(max_length=50)
    Events_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_Events'
        verbose_name = "告警信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.EventName


#  3、<Commands>控制信息表
class Commands(models.Model):
    EquipTemplateId = models.CharField(max_length=50)
    EquipTemplateName = models.CharField(max_length=50)
    EquipTemplateType = models.CharField(max_length=50)
    LibName = models.CharField(max_length=50)

    CommandId = models.CharField(max_length=50)
    CommandName = models.CharField(max_length=150)
    CommandToken = models.CharField(max_length=50)
    ParameterId = models.CharField(max_length=50)
    ParameterName = models.CharField(max_length=50)
    ParameterValue = models.CharField(max_length=50)
    Meaning = models.CharField(max_length=50)

    Commands_ip = models.CharField(max_length=50)
    Commands_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_Commands'
        verbose_name = "控制信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ParameterName
