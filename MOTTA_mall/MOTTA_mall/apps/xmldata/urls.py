from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^websocket', views.websocket),
    url(r'^querywebsocket', views.QueryWebsocket),

]
