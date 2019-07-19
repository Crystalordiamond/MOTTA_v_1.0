from django.contrib.auth.models import AbstractUser
from django.db import models
from . import constants
from utils import tjws


class User(AbstractUser):
    # 默认拥有了用户名、密码、邮箱等属性
    # 扩展属性：定义
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name="邮箱认证")
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_url(self):
        # 生成校验网址
        # 构造有效数据
        data = {'user_id': self.id}
        # 加密
        token = tjws.dumps(data, constants.VERIFY_EMAIL_EXPIRES)
        # 构造激活链接
        return 'http://www.motta.site:8080/success_verify_email.html?token=' + token


