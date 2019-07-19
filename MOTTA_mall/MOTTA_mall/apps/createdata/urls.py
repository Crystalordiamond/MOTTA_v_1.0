from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^warning_config_get/$', views.get_addconfig),
    url(r'^warning_config_put/$', views.post_addconfig),
]
