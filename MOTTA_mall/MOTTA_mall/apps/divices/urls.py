from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^All_site/$', views.All_site),  # 查询站点
    url(r'^newaddress_user/$', views.get_address_user), # 查询用户
    url(r'^newaddress/$', views.post_newAddress), # 新增站点
    url(r'^newuser/$', views.post_newUser), # 新增用户
    url(r'^ondelete_user/$', views.post_delete_user), # 删除用户
    url(r'^ondelete_address/$', views.post_delete_address), # 删除站点
    url(r'^onmodify_user/$', views.put_user), # 修改用户
    url(r'^onmodify_address/$', views.put_address), # 修改用户
    url(r'^coordinate/$', views.coordinate_post), # 存入坐标点
    url(r'^coordinate_get/$', views.coordinate_get), # 查询坐标点
    url(r'^coordinateDelete/$', views.coordinateDelete), # 删除坐标点
    url(r'^coordinateUpdate/$', views.coordinateUpdate), # 修改坐标点
    url(r'^cameras/$', views.cameras_get), #  获取摄像头列表
    url(r'^cameras_post/$', views.cameras_post),
    url(r'^cameras_delete/$', views.cameras_delete),
    url(r'^cameras_update/$', views.cameras_update),
    url(r'^email_get/$', views.email_get),
    url(r'^email_update/$', views.email_update),
    url(r'^email_test/$', views.email_test),
    url(r'^details_get/$', views.details_get), # 获取详情页面的MDC列表
    url(r'^sql_data/$', views.sql_post), # 下载sql表结构
    url(r'^sql_put/$', views.sql_put), # 保上传ql表结构
    url(r'^site_name/$', views.SiteName), # 查询对应站点的设备数量名称

]
