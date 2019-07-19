from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^users/$', views.UserCreateView.as_view()),  # 注册用户
    url(r'^authorizations/$', obtain_jwt_token), # Django REST framework JWT提供了登录签发JWT的视图，可以直接使用
    url(r'^user/$', views.UserDetailView.as_view()), # 用户详细信息  需登入
    # url(r'^userout/$', views.UserLogoutView.as_view()), # 用户退出
    url(r'^emails/$', views.EmailView.as_view()),
    url(r'^emails/verification/$', views.EmailActiveView.as_view()),
]

