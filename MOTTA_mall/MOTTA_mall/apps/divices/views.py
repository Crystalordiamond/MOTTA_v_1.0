import os

from django.http.response import JsonResponse
from rbac.models import User
from warning.models import AlarmContent, HistoryData, Warning
from xmldata.models import XmlData, port, equipments, logactions, Signals_meaing, Events, Commands
from .models import divices, Cameras, coordinate, WarningConfig
from django.db.models import Q, F
from django.http import HttpResponse
import json
from django.core.mail import send_mail
from django.conf import settings
from pymysql import connect
import xmldata.constants as cons


# 0.将坐标点存入数据库
def coordinate_post(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6 无需执行此步
    coor_data = json.loads(json_str)
    coor_list = coordinate.objects.filter(coordinate_ip=coor_data['ip'])
    if coor_list:
        return JsonResponse({'status': 'no'})
    else:
        try:
            coordinate.objects.create(
                coordinate_ip=coor_data['ip'],
                coordinate_location=coor_data['location'],
                coordinate_site=coor_data['site'],
                coordinate_A=coor_data['A'],
                coordinate_B=coor_data['B'],
                coordinate_address=coor_data['address']
            )
            return JsonResponse({'status': 'yes'})
        except:
            return JsonResponse({'status': 'no'})


# 0.查询坐标点
def coordinate_get(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6 无需执行此步
    coor_data = json.loads(json_str)
    coor_list = coordinate.objects.filter(coordinate_ip__in=coor_data['ip'])
    coordinate_list = []
    for i in coor_list:
        dict_data = {
            "location": i.coordinate_location,
            "site": i.coordinate_site,
            # 存入坐标点时候，没有保存status
            "status": "Normal",
            # 加一个颜色字段 蓝色
            "colour": "#000080",
            "A": i.coordinate_A,
            "B": i.coordinate_B,
            "address": i.coordinate_address,
            'users': [i["username"] for i in
                      divices.objects.filter(divice_ip=i.coordinate_ip)[0].user_id.all().values('username')]
        }
        coordinate_list.append(dict_data)
    return JsonResponse(coordinate_list, safe=False)


# 0.删除坐标点
def coordinateDelete(request):
    json_str = request.body.decode()
    coordinate_data = json.loads(json_str)
    # print('coordinate_data', coordinate_data)
    coordinate.objects.filter(coordinate_site=coordinate_data["site"]).delete()  # 删除
    return JsonResponse("Coordinate point deleted successfully", safe=False)


# 0.更新坐标点
def coordinateUpdate(request):
    json_str = request.body.decode()
    coordinate_data = json.loads(json_str)
    print('coordinate_data', coordinate_data)
    coordinate.objects.filter(coordinate_site=coordinate_data["site"]).update(
        coordinate_address=coordinate_data['address']
    )
    return JsonResponse("Coordinate address updated successfully", safe=False)


# 1.新增用户
def post_newUser(request):
    json_str = request.body.decode()
    user_data = json.loads(json_str)
    print(user_data)
    if User.objects.filter(username=user_data["account"]):
        return JsonResponse("The username already exists", safe=False)
    # 1.存储user用户数据
    """必须使用Django自带的username，使用自定义的username第一次创建username可以为空，第二创建还为空，就会报错username重复"""
    user_obj = User.objects.create(
        username=user_data["account"],
        u_backup=user_data["grade"],
        password=user_data["password"],
        u_phone=user_data["phone"],
        email=user_data["email"]
    )
    # 2.存储user用户和与之关联的站点
    """
    1.多对多表的查询逻辑 （针对manytomany字段） 只在一边做处理，
    2.没有manytomany字段的表 就获取另外一张表的对象来点add(里面是要存储的对象)
    """
    # 创建用户 传过来的是设备的ID("user_address")
    # print(user_data["site"])
    if user_data.get("site"):
        divices_obj = divices.objects.filter(id__in=user_data["site"]).all()
        for divice in divices_obj:
            divice.user_id.add(user_obj)
    return JsonResponse("User creation complete", safe=False)


# 2.新增站点
def post_newAddress(request):
    json_str = request.body.decode()
    divices_data = json.loads(json_str)
    print('1111111111111111111', divices_data)
    if divices.objects.filter(divice_ip=divices_data["ip"]) or divices.objects.filter(divice_site=divices_data["site"]):
        return JsonResponse("The IP address or Site already exists", safe=False)
    # 1.创建站点对象
    divices_obj = divices.objects.create(
        divice_ip=divices_data["ip"],
        divice_location=divices_data["location"],
        divice_site=divices_data["site"],
        divice_communication=divices_data["communication"],
        divice_type=divices_data["type"],
        divice_serial=divices_data["serial"],
    )
    # 2.通过站点对象的user_id字段添加关联的站点
    """
    这是在含有manytomany字段的表
    1.先查询传过来的user的id("divices_data["addUser"]")
    2.得到user对象
    3.通过多对多字段添加
    字典.get("addUser")  get key不存在不会报错
    """
    if divices_data.get("addUser"):
        print(divices_data["addUser"])
        # 查询传过来的用户 divices_data["addUser"] 得到的是用户id
        user_obj = User.objects.filter(id__in=divices_data["addUser"]).all()
        for obj in user_obj:
            divices_obj.user_id.add(obj)
    return JsonResponse("Site created successfully", safe=False)


# 3.获取设备站点信息 url :All_site
def All_site(request):
    json_str = request.body
    json_str = json_str.decode()
    site_data = json.loads(json_str)
    # print("All_site:",site_data)
    # 1.超级管理员 获取所有信息
    if site_data['grade'] == 'Administrator':
        list_data = []
        # 1.1 超级管理员直接查询所有站点
        address_obj = divices.objects.all()
        # 1.2 遍历站点对象
        for address in address_obj:
            manage_list = []
            # 1.3 通过站点对象，通过user_id这个ManyToManyField字段正向查询该站点有哪一些用户
            for i in address.user_id.all().values("username"):
                # 1.4 将站点关联的用户存入列表
                manage_list.append(i["username"])
            # 1.5 构造dict对象
            data_dict = {
                "id": address.id,
                "site": address.divice_site,
                "location": address.divice_location,
                "ip": address.divice_ip,
                "communication": address.divice_communication,
                "type": address.divice_type,
                "serial": address.divice_serial,
                "manager": ','.join(manage_list)
            }
            # 1.6 构造json数据格式对象
            list_data.append(data_dict)
        # 1.7 发送json数据到前端
        return JsonResponse(list_data, safe=False)
    # 2.普通用户获取 用户信息
    else:
        list_data = []
        # 2.1 查询到用户对象
        user_object = User.objects.filter(username=site_data['user'])
        # 2.2 通过divices_set反向查询，得到该用户管理哪一些站点
        address_obj = user_object[0].divices_set.all()
        for address in address_obj:
            manage_list = []
            # 2.3 通过站点正向查询，每个站点有哪一些用户管理员
            for i in address.user_id.all().values("username"):
                # 2.4 得到管理员列表
                manage_list.append(i["username"])
            data_dict = {
                "id": address.id,
                "site": address.divice_site,
                "location": address.divice_location,
                "ip": address.divice_ip,
                "communication": address.divice_communication,
                "type": address.divice_type,
                "serial": address.divice_serial,
                "manager": ','.join(manage_list)
            }
            # 2.5 构造json数据格式对象
            list_data.append(data_dict)
        # 2.6 发送json数据到前端
        return JsonResponse(list_data, safe=False)


# 4.获取用户信息
def get_address_user(request):
    user_obj = User.objects.filter().all()
    list_data = []
    for users in user_obj:
        # print(users.u_backup)
        # 除了超级管理员其他的管理员都展示
        # if not users.u_backup == 'Administrator':
        data_dict = {"id": users.id,
                     "account": users.username,
                     "grade": users.u_backup,
                     "password": users.password,
                     "phone": users.u_phone,
                     "email": users.email,
                     "site": ','.join([i.divice_site for i in users.divices_set.all()])
                     }
        list_data.append(data_dict)
    return JsonResponse(list_data, safe=False)


# 删除用户
def post_delete_user(request):
    user_str = request.body.decode()  # 字符串
    req_data = json.loads(user_str)  # 字典
    # print(req_data)
    user_obj = User.objects.get(username=req_data["account"])
    # divices_set反向查询：  或者divices.object.filter()
    user_obj.divices_set.clear()  # 删除用户站点的关联关系
    user_obj.delete()  # 删除用户
    return JsonResponse("User deleted successfully", safe=False)


# 删除站点
def post_delete_address(request):
    address_str = request.body.decode()  # 字符串
    req_data = json.loads(address_str)  # 字典
    # print(req_data)
    address_obj = divices.objects.get(divice_ip=req_data["ip"])
    # print(address_obj)
    # 1.删除站点的关联关系
    address_obj.user_id.clear()
    # 2.删除站点
    address_obj.delete()
    # 3.删除对应的坐标点
    coordinate.objects.filter(coordinate_ip=req_data["ip"]).delete()
    # 4.删除AlarmContent的数据
    AlarmContent.objects.filter(alarm_ip=req_data["ip"]).delete()
    # 5.删除历史告警的数据
    Warning.objects.filter(warn_ip=req_data["ip"]).delete()
    # 6.删除历史数据
    HistoryData.objects.filter(equipment_ip=req_data["ip"]).delete()
    # 7.删除xmldata表的关联
    XmlData.objects.filter(divice_ip=req_data["ip"]).delete()
    port.objects.filter(port_ip=req_data["ip"]).delete()
    equipments.objects.filter(Equipment_ip=req_data["ip"]).delete()
    logactions.objects.filter(logactions_ip=req_data["ip"]).delete()
    Signals_meaing.objects.filter(Signals_ip=req_data["ip"]).delete()
    Events.objects.filter(Events_ip=req_data["ip"]).delete()
    Commands.objects.filter(Commands_ip=req_data["ip"]).delete()
    Cameras.objects.filter(cam_ip=req_data["ip"]).delete()
    return JsonResponse("Site deleted successfully", safe=False)


# 修改用户信息
def put_user(request):
    json_str = request.body.decode()  # 字符串
    user_data = json.loads(json_str)  # 字符串转字典
    # print(user_data)
    """1.先删除原有的用户及其关联"""
    user_obj = User.objects.get(username=user_data["account"])
    user_obj.divices_set.clear()  # 删除用户站点的关联关系
    # user_obj.delete()  # 删除用户
    """2.再更新用户"""
    User.objects.filter(username=user_data["account"]).update(
        username=user_data["account"],
        u_backup=user_data["grade"],
        password=user_data["password"],
        u_phone=user_data["phone"],
        email=user_data["email"]
    )
    """
    3.将更新的用户关联站点
        3.1 多对多表的查询逻辑 （针对manytomany字段） 只在一边做处理，
        3.2 没有manytomany字段的表 就获取另外一张表的对象来点add(里面是要存储的对象)
    """
    # 创建用户 传过来的是设备的ID("site") todo 有时候不是设备id
    if user_data.get("site"):
        print(user_data["site"])
        # divices_obj = divices.objects.filter(id__in=user_data["site"]).all()
        divices_obj = divices.objects.filter(divice_site__in=user_data["site"]).all()
        # print(divices_obj)
        for divice in divices_obj:
            divice.user_id.add(user_obj)
    return JsonResponse("User modified successfully", safe=False)


# 修改站点信息
def put_address(request):
    json_str = request.body.decode()
    divices_data = json.loads(json_str)
    ip = divices.objects.get(divice_site=divices_data["site"]).divice_ip
    """如果ip没有修改 无需核对是否重复"""
    if ip == divices_data["ip"]:
        # 1.查询到对象
        address_obj = divices.objects.get(divice_site=divices_data["site"])
        # 2.删除对象的关联关系
        address_obj.user_id.clear()
        # 3.更新对象(get()方法和filter()方法)
        divices.objects.filter(divice_site=divices_data["site"]).update(
            divice_ip=divices_data["ip"],
            divice_location=divices_data["location"],
            divice_site=divices_data["site"],
            divice_communication=divices_data["communication"],
            divice_type=divices_data["type"],
            divice_serial=divices_data["serial"],
        )
        # 4.设置对象的关联关系
        if divices_data.get("addUser"):
            print(divices_data["addUser"])
            # 查询传过来的用户 传过来的都是id
            user_obj = User.objects.filter(id__in=divices_data["addUser"]).all()
            for obj in user_obj:
                address_obj.user_id.add(obj)
        return JsonResponse("Site modified successfully", safe=False)
    else:
        """如果ip修改 查询ip是否重复"""
        if divices.objects.filter(divice_ip=divices_data["ip"]):
            return JsonResponse("IP address already exists", safe=False)
        # 1.查询到对象
        address_obj = divices.objects.get(divice_site=divices_data["site"])
        # 2.删除对象的关联关系
        address_obj.user_id.clear()
        # 3.更新对象(get()方法和filter()方法)
        divices.objects.filter(divice_site=divices_data["site"]).update(
            divice_ip=divices_data["ip"],
            divice_location=divices_data["location"],
            divice_site=divices_data["site"],
            divice_communication=divices_data["communication"],
            divice_type=divices_data["type"],
            divice_serial=divices_data["serial"],
        )
        # 4.设置对象的关联关系
        if divices_data.get("addUser"):
            print(divices_data["addUser"])
            # 查询传过来的用户 传过来的都是id
            user_obj = User.objects.filter(id__in=divices_data["addUser"]).all()
            for obj in user_obj:
                address_obj.user_id.add(obj)
        return JsonResponse("Site modified successfully", safe=False)


# 摄像头的 查 增 删 改
def cameras_get(request):
    cameras_obj = Cameras.objects.all()
    cameras_list = []
    for i in cameras_obj:
        cameras_dict = {
            "site": i.cam_site,
            "location": i.cam_location,
            "camerasAdds": i.cam_address,
            "ip": i.cam_ip
        }
        cameras_list.append(cameras_dict)
    return JsonResponse(cameras_list, safe=False)


def cameras_post(request):
    json_str = request.body.decode()
    cameras_data = json.loads(json_str)
    # print('11111111111111111111111', cameras_data)
    Cameras.objects.create(
        cam_site=cameras_data["site"],
        cam_location=cameras_data["location"],
        cam_address=cameras_data["camerasAdds"]
    )
    return JsonResponse("Cameras created successfully", safe=False)


def cameras_delete(request):
    user_str = request.body.decode()  # 字符串
    cameras_data = json.loads(user_str)  # 字典
    # print(req_data)
    cameras_obj = Cameras.objects.filter(cam_site=cameras_data["site"])
    cameras_obj.delete()  # 删除用户
    return JsonResponse("Cameras deleted successfully", safe=False)


def cameras_update(request):
    json_str = request.body.decode()
    cameras_data = json.loads(json_str)
    # print('11111111111111111111111', cameras_data)
    Cameras.objects.filter(cam_site=cameras_data["site"]).update(
        cam_location=cameras_data["location"],
        cam_address=cameras_data["camerasAdds"]
    )
    return JsonResponse("Cameras modified successfully", safe=False)


# 邮件的增 改 测试
def email_get(request):
    email_data = WarningConfig.objects.all().first()
    # print(email_data)
    data_dict = {
        "server": email_data.con_server,
        "port": email_data.con_port,
        "method": email_data.con_method,
        "account": email_data.con_account,
        "password": email_data.con_password
    }
    return JsonResponse(data_dict, safe=False)


def email_update(request):
    email_data = request.body.decode()
    email_str = json.loads(email_data)
    print(email_str)
    data = WarningConfig.objects.filter(con_other=email_str["grade"])
    print(data)
    if data:
        data.update(
            con_server=email_str["server"],
            con_port=email_str["port"],
            con_method=email_str["method"],
            con_account=email_str["account"],
            con_password=email_str["password"],

        )
    else:
        data.create(
            con_server=email_str["server"],
            con_port=email_str["port"],
            con_method=email_str["method"],
            con_account=email_str["account"],
            con_password=email_str["password"],
            con_other=email_str["grade"]
        )
    return JsonResponse("update successfully", safe=False)


def email_test(request):
    email_data = request.body.decode()
    email_str = json.loads(email_data)
    # print(email_str["test"])
    # print(settings.EMAIL_HOST_USER)
    # print(type(email_str["test"]))
    send_mail("The alarm mail", "This is the test email", settings.EMAIL_HOST_USER, [email_str["test"]], "")
    return JsonResponse("Email sent successfully", safe=False)


# 获取详情页面的MDC列表
def details_get(request):
    details_user = request.body.decode()
    details_str = json.loads(details_user)
    details_data = User.objects.filter(username=details_str["username"])
    site_list = []
    for address in details_data[0].divices_set.all():
        data_dict = {
            "id": address.id,
            "site": address.divice_site,
            "location": address.divice_location,
            "ip": address.divice_ip,
            "communication": address.divice_communication,
            "type": address.divice_type,
            "serial": address.divice_serial,
            "manager": [i['username'] for i in address.user_id.all().values("username")]
        }
        site_list.append(data_dict)
    return JsonResponse(site_list, safe=False)


# 保存sql表结构
def sql_post(request):
    sql_data = request.body.decode()
    sql_str = json.loads(sql_data)
    # print(sql_str)
    # 1.将数据表结构保存到当前文件夹
    # os.system('mysqldump -h localhost -uroot -pmysql -d MOTTA_data > dump.sql')
    os.system('mysqldump -h localhost -uroot -pmysql  MOTTA_data tb_user tb_divices tb_warningconfig > dump.sql')
    # 2.读取sql文件，并返回给前端
    try:
        f_name = open('./dump.sql', 'r', encoding='UTF-8').read()
        return JsonResponse(f_name, safe=False)
    except OSError as reason:
        print('读取文件出错了：%s' % str(reason))


def sql_put(request):
    data = request.FILES.get('file')
    print(data)
    with open('./dump.sql', 'wb') as f:
        for i in data:
            f.write(i)
    os.system('mysql -uroot -pmysql  MOTTA_data< dump.sql')
    return JsonResponse("ok", safe=False)


# 查询对应站点的设备数量名称
def SiteName(request):
    json_str = request.body.decode()
    site_data = json.loads(json_str)
    site_obj = []
    # 遍历得到ip
    for i in site_data['site']:
        UPS = []
        TH = []
        AC = []
        Meter = []
        VTU = []
        # 通过ip查找设备
        equiment_list = equipments.objects.filter(Equipment_ip=i)
        # 有一些新添加的站点没有设备，需要过滤一下，判断列表不为空
        if len(equiment_list) != 0:
            for j in equiment_list:
                if j.LibName in cons.ups_type:
                    UPS.append(j.EquipmentName)
                elif j.LibName in cons.TH_type:
                    TH.append(j.EquipmentName)
                elif j.LibName in cons.Meter_type:
                    Meter.append(j.EquipmentName)
                elif j.LibName in cons.AC_type:
                    AC.append(j.EquipmentName)
                elif j.LibName in cons.VTU_type:
                    VTU.append(j.EquipmentName)
            if Meter:
                UPS.append("Power")
            site_dict = {
                    "site": divices.objects.filter(divice_ip=i)[0].divice_site,
                    "UPS": UPS,
                    "TH": TH,
                    "Meter": Meter,
                    "AC": AC,
                    "VTU": VTU,
                    "ip":i
                }
            site_obj.append(site_dict)
    return JsonResponse(site_obj, safe=False)


"""  
在Pyhton里有一个叫simplejson的库可以方便的将完成对json的生成与解析。
这个包里主要有四个方法：dump和dumps由python数据类型生成json，load和loads将json解析成为python的数据类型。                  
dump和dumps的唯一区别是dump会生成一个类文件对象，dumps会生成字符串，
load和loads的唯一区别是load解析类文件对象，loads解析字符串格式的JSON，
    在django的HttpResponse中的返回中需要将字典类型转为json字符串，通常为HttpRespons（json.dumps(response))
    或者直接使用django里的JsonRespnse（respnse）来返回数据。
却别在于HttpResponse需要我们自己前后台进行序列化parse()与反序列化stringify(),而JasonResponse则把序列化和反序列化封装了起来，我们直接传入可序列化
        
"""
