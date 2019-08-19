from django.db import models
from users.models import User
# from createdata.models import AddressConfig


class divices(models.Model):
    divice_ip = models.CharField(max_length=50, verbose_name='ip地址', unique=True)
    divice_name = models.EmailField(max_length=50, verbose_name='站点名称')
    divice_email = models.EmailField(max_length=50, verbose_name='站点邮箱')
    divice_phone = models.CharField(max_length=50, verbose_name="站点电话")
    divice_other = models.CharField(max_length=50, verbose_name="其他")
    is_delete = models.IntegerField(default=False, verbose_name='逻辑删除')
    # AddressConfig = models.ForeignKey(AddressConfig, on_delete=models.CASCADE, verbose_name='关联告警配置')
    user_id = models.ManyToManyField(to=User)

    class Meta:
        db_table = 'tb_divices'
        verbose_name = '站点信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.divice_name




