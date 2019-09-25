from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^newuser/$', views.post_newUser),
    url(r'^newuser_address/$', views.get_newuser_addresss),
    url(r'^newaddress/$', views.post_newAddress),
    url(r'^newaddress_user/$', views.get_address_user),
    url(r'^ondelete_user/$', views.post_delete_user),
    url(r'^ondelete_address/$', views.post_delete_address),
    url(r'^onmodify_user/$', views.put_user),
    url(r'^onmodify_address/$', views.put_address),
    url(r'^user_login/$', views.post_login),

]
