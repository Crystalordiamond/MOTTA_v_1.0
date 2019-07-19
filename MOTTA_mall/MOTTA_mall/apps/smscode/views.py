import random

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code
from . import constants


class SMSCodeView(APIView):
    def get(self, request, mobile):
        # 限制60秒只向一个手机号发送一次短信验证码
        # 获取redis链接
        redis_cli = get_redis_connection('sms_code')
        # 判断60秒内是不是指定手机号法发过短信，如果发过则抛异常
        if redis_cli.get('sms_flag_' + mobile):
            raise serializers.ValidationError('向此手机号发短信太频繁了')
        code = random.randint(100000, 999999)
        # setex存储数据
        # redis_cli.setex('sms_code_' + mobile, 300, code)
        # redis_cli.setex('sms_flag_' + mobile, 60, 1)
        # 优化：pipeline管道  减少和redis的交互 先将命令放入到管道然后一次性统一执行，就是和redis交互一次
        redis_pipeline = redis_cli.pipeline()
        redis_pipeline.setex('sms_code_' + mobile, constants.SMS_CODE_EXPIRES, code)
        redis_pipeline.setex('sms_flag_' + mobile, constants.SMS_FLAG_EXPIRES, 1)
        redis_pipeline.execute()
        # CCP.sendTemplateSMS(mobile, code, constants.SMS_CODE_EXPIRES / 60, 1)
        # print(code)
        # 调用celery任务，执行耗时代码  通过delay函数将任务放在另一个进程中执行
        send_sms_code.delay(mobile, code, constants.SMS_CODE_EXPIRES / 60, 1)
        return Response({'message': 'OK'})
