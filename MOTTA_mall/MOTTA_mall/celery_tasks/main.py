from celery import Celery

import os

# 为celery使用django配置文件进行设置
os.environ.setdefault("DJANGO_SETTING_MODULE", "MOTTA_mall.settings.dev")

# MOTTA_mall项目文件夹
app = Celery('MOTTA_mall')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks([
    'celery_tasks.email',
    'celery_tasks.sms',
])