from django.conf.urls import url, include

from . import views

urlpatterns = [

    # url(r'^baseapi', include("baseapp.urls")),
    url(r'^.*?$', views.index, name='index')

]
