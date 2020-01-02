from django.core.mail import send_mail
from celery_tasks.main import app
from django.conf import settings


@app.task(name='send_verify_mail')
def send_verify_mail(to_email, html_message):
    subject = "MOTTA邮件告警"
    send_mail(subject, '', settings.EMAIL_HOST_USER, to_email, html_message=html_message)

# from django.conf import settings
# from django.core.mail import send_mail
# from celery_tasks.main import app
#
#
# @app.task(name='send_verify_mail')
# def send_verify_mail(to_email, html_msg):
#     # print(to_email)
#     # # print(html_msg)
#     subject = "邮件告警"
#     # send_mail(subject, '', settings.EMAIL_HOST_USER, to_email, html_message=html_msg)
#     send_mail(subject, '', 'luochenxi163@163.com', to_email, html_message=html_msg)
