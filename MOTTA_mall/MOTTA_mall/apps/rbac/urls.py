from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user_login/$', views.post_login),
    url(r'^out_put/$', views.out_put),
    url(r'^userstatus_post/$', views.userstatus_post),
    url(r'^password_verily/$', views.password_verily),
]
