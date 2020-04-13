from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^websocket', views.websocket),  # 这是发送过来的get请求signaldata
    url(r'^querywebsocket', views.QueryWebsocket),
    url(r'^GetWebsocket', views.GetWebsocket),
    url(r'^PostWebsocket', views.PostWebsocket),

]
