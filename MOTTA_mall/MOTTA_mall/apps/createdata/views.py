from .models import AddressConfig
from divices.models import divices
from django.http.response import JsonResponse
import json


# 获取告警配置信息
def get_addconfig(request):
    json_str = request.body.decode()
    address_data = json.loads(json_str)
    # print(address_data)
    list_data = []
    # print(ip_data)
    # divice_obj = divices.objects.filter(divice_ip=address_data["ip_address"])
    # print(divice_obj)
    add_obj = AddressConfig.objects.get(divices=address_data["ip_address"])
    # print(add_obj.server_address)
    if add_obj:
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
    if AddressConfig.objects.filter(divice_ip=address_data["ip_address"]) != []:
        print(AddressConfig.objects.get().divices.divice_ip)
        AddressConfig.objects.filter(divice_ip=address_data["ip_address"]).update(
            server_address=address_data["server_address"],
            port_config=address_data["port_config"],
            send_mail=address_data["send_mail"],
            password=address_data["password"],
            COM_phone=address_data["COM_phone"]
        )
    if AddressConfig.objects.filter(divice_ip=address_data["ip_address"]) == []:
        divices_obj = divices.objects.filter(divice_ip=address_data["ip_address"]).first()
        AddressConfig.objects.create(
            server_address=address_data["server_address"],
            port_config=address_data["port_config"],
            send_mail=address_data["send_mail"],
            password=address_data["password"],
            COM_phone=address_data["COM_phone"],
            divice_ip=address_data["ip_address"],
            divices=divices_obj
        )
    return JsonResponse("配置完成", safe=False)
