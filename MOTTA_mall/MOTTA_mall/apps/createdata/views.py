from .models import AddressConfig
from divices.models import divices
from django.http.response import JsonResponse
import json


# 获取告警配置信息
def get_addconfig(request):
    # json_str = request.body.decode()
    # address_data = json.loads(json_str)
    # print(address_data["ip_address"])
    list_data = []
    add_obj = AddressConfig.objects.filter().first()
    # print(add_obj)   #打印是否为None
    """
    1.数据库没有站点时候，查询返回的是None
    2.数据库有站点，没有配置信息时候返回的是None
    """
    if add_obj != None:
        data_dict = {
            "server_address": add_obj.server_address,
            "port_config": add_obj.port_config,
            "send_mail": add_obj.send_mail,
            "password": add_obj.password,
            "COM_phone": add_obj.COM_phone,
            "other_config": add_obj.other_config
        }
        list_data.append(data_dict)
    return JsonResponse(list_data, safe=False)


# 告警配置
def post_addconfig(request):
    json_str = request.body.decode()
    address_data = json.loads(json_str)
    print(address_data)
    if AddressConfig.objects.filter().first() == None:
        divices_obj = divices.objects.filter().first()
        print(divices_obj)
        AddressConfig.objects.create(
            server_address=address_data["server_address"],
            port_config=address_data["port_config"],
            send_mail=address_data["send_mail"],
            password=address_data["password"],
            COM_phone=address_data["COM_phone"],
            other_config=address_data["other_config"],
            divices=divices_obj
        )
    else:
        print(AddressConfig.objects.filter().first())
        AddressConfig.objects.filter().update(
            server_address=address_data["server_address"],
            port_config=address_data["port_config"],
            send_mail=address_data["send_mail"],
            password=address_data["password"],
            COM_phone=address_data["COM_phone"]
        )

    return JsonResponse("配置完成", safe=False)


# 获取页脚数据
def get_bar(request):
    ip_str = request.GET.get("ip")  # <class 'str'>类型
    divice_obj = divices.objects.filter(divice_ip=ip_str)
    # data_dict = {}
    # if list(divice_obj) != []:
    data_dict = {
        "add_name": divice_obj.first().divice_name,
        "username": list(divice_obj.first().user_id.all().values('username')),  # 通过list，将查询对象Queryset转化成lsit
        "mobile": list(divice_obj.first().user_id.all().values('mobile')),
        "email": list(divice_obj.first().user_id.all().values('email')),
    }
    # json_data = json.dumps(data_dict)
    return JsonResponse(data_dict, safe=False)
