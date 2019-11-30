from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user_login/$', views.post_login),
]
