from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^selectequipment/$', views.get_equipment),
    url(r'^historydata/$', views.post_historydata),
    url(r'^historyalarm/$', views.post_historyalarm),

]
