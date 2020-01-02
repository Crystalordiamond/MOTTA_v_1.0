from celery import Celery
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'MOTTA_mall.settings.dev'

# MOTTA_mall项目文件夹
app = Celery('MOTTA_mall')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks([
    'celery_tasks.email',
    'celery_tasks.sms',
])