from django.http.response import JsonResponse
from users.models import User
from divices.models import divices
from django.db.models import Q, F
from django.http import HttpResponse
import json


# 1.新增用户
def post_newUser(request):
    json_str = request.body.decode()
    user_data = json.loads(json_str)
    print(user_data)
    # 1.存储user用户数据
    user_obj = User.objects.create(
        is_superuser=user_data["level"],
        username=user_data["user"],
        password=user_data["password"],
        email=user_data["email"],
        mobile=user_data["phone"]
    )
    # 2.存储user用户和与之关联的站点
    """
    1.多对多表的查询逻辑 （针对manytomany字段） 只在一边做处理，
    2.没有manytomany字段的表 就获取另外一张表的对象来点add(里面是要存储的对象)
    """
    # 创建用户 传过来的是设备的ID("user_address")
    if user_data["site"] != []:
        divices_obj = divices.objects.filter(id__in=user_data["site"]).all()
        for divice in divices_obj:
            divice.user_id.add(user_obj)
    return JsonResponse("用户创建完成", safe=False)


# 2.新增站点
def post_newAddress(request):
    json_str = request.body.decode()
    divices_data = json.loads(json_str)
    # 1.创建站点对象
    divices_obj = divices.objects.create(
        divice_ip=divices_data["ip"],
        divice_name=divices_data["address"],
    )
    # 2.通过站点对象的user_id字段添加关联的站点
    """
    这是在含有manytomany字段的表
    1.先查询传过来的user的id("divices_data["addUser"]")
    2.得到user对象
    3.通过多对多字段添加
    """
    if divices_data["addUser"] != []:
        # print(divices_data["addUser"])
        # 查询传过来的用户
        user_obj = User.objects.filter(id__in=divices_data["addUser"]).all()
        for obj in user_obj:
            divices_obj.user_id.add(obj)
    return JsonResponse("站点创建完成", safe=False)


# 1.1获取设备站点信息
def get_newuser_addresss(request):
    address_obj = divices.objects.all()
    list_data = []
    for address in address_obj:
        id = address.id
        site = address.divice_name
        # 上面两条信息 在新增用户时候需要用到
        ip = address.divice_ip
        email_add = address.divice_email
        phone_add = address.divice_phone
        # 关联用户 通过关联字段查询出所有，然后查询到指定的username 由于是Qset对象
        username_add = []  # 站点关联的用户
        username_list = address.user_id.all().values("username")
        # print(username_list)
        for i in username_list:
            username_add.append(i["username"])
        data_dict = {"id": id,
                     "address": site,
                     "ip": ip,
                     "add_email": email_add,
                     "add_phone": phone_add,
                     "addUser": username_add
                     }
        list_data.append(data_dict)
    return JsonResponse(list_data, safe=False)
    # return JsonResponse("ok", safe=False)


# 2.1获取用户信息
def get_address_user(request):
    user_obj = User.objects.filter().all()
    list_data = []
    for users in user_obj:
        id = users.id
        user = users.username
        # 上面两条信息 在新增站点时候需要用到
        level = "超级管理员" if users.is_superuser == True else "一般管理员"
        # print(level)
        email = users.email
        phone = users.mobile
        # 获取关联的站点列表
        # todo
        site_list = []
        site = users.divices_set.all()
        print(site)
        for i in site:
            print(i)
            site_list.append(i.divice_name)
        print(site_list)
        data_dict = {"id": id,
                     "user": user,
                     "level": level,
                     "site": site_list,
                     "email": email,
                     "phone": phone
                     }
        list_data.append(data_dict)
    return JsonResponse(list_data, safe=False)

# 删除用户
def post_delete_user(request):
    user_str = request.body.decode()  # 字符串
    req_data = json.loads(user_str)  # 字典
    # print(req_data)
    user_obj = User.objects.get(username=req_data["user"])
    # divices_set反向查询：  或者divices.object.filter()
    user_obj.divices_set.clear()  # 删除用户站点的关联关系
    user_obj.delete()  # 删除用户
    return JsonResponse("用户删除成功", safe=False)


# 删除站点
def post_delete_address(request):
    address_str = request.body.decode()  # 字符串
    req_data = json.loads(address_str)  # 字典
    # print(req_data)
    address_obj = divices.objects.get(id=req_data["id"])
    # print(address_obj)
    address_obj.user_id.clear()  # 删除站点的关联关系
    address_obj.delete()  # 删除站点
    return JsonResponse("站点删除成功", safe=False)


# 修改用户信息
def put_user(request):
    json_str = request.body.decode()  # 字符串
    user_data = json.loads(json_str)  # 字符串转字典
    # print(user_data)
    # level默认传过来的是“超级管理员”或者“一般管理员”  修改后传过来的是“1”，“0”
    user_data["level"] = "1" if user_data["level"] == "超级管理员" else "0"
    """1.先删除原有的用户及其关联"""
    user_obj = User.objects.get(username=user_data["user"])
    user_obj.divices_set.clear()  # 删除用户站点的关联关系
    # user_obj.delete()  # 删除用户
    """2.再更新用户"""
    User.objects.filter(username=user_data["user"]).update(
        is_superuser=user_data["level"],
        username=user_data["user"],
        email=user_data["email"],
        mobile=user_data["phone"]
    )
    """
    3.将更新的用户关联站点
        3.1 多对多表的查询逻辑 （针对manytomany字段） 只在一边做处理，
        3.2 没有manytomany字段的表 就获取另外一张表的对象来点add(里面是要存储的对象)
    """
    # 创建用户 传过来的是设备的ID("site")
    if user_data["site"] != []:
        # print(user_data["site"])
        # divices_obj = divices.objects.filter(id__in=user_data["site"]).all()
        divices_obj = divices.objects.filter(Q(id__in=user_data["site"]) | Q(divice_name__in=user_data["site"])).all()
        # print(divices_obj)
        for divice in divices_obj:
            divice.user_id.add(user_obj)
    return JsonResponse("修改用户信息成功", safe=False)


# 修改站点信息
def put_address(request):
    json_str = request.body.decode()
    divices_data = json.loads(json_str)
    # 1.查询到对象
    address_obj = divices.objects.get(divice_ip=divices_data["ip"])
    # 2.删除对象的关联关系
    address_obj.user_id.clear()
    # 3.更新对象(get()方法和filter()方法)
    divices.objects.filter(divice_ip=divices_data["ip"]).update(
        # divice_ip=divices_data["ip"],
        divice_name=divices_data["address"],
        divice_email=divices_data["add_email"],
        divice_phone=divices_data["add_phone"]
    )
    # 4.设置对象的关联关系
    if divices_data["addUser"] != []:
        # print(divices_data["addUser"])
        # 查询传过来的用户
        user_obj = User.objects.filter(id__in=divices_data["addUser"]).all()
        for obj in user_obj:
            address_obj.user_id.add(obj)
    return JsonResponse("站点创建完成", safe=False)

