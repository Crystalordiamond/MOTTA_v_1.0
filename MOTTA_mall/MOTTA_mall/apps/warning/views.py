import random
import re

from django.http.response import JsonResponse
from django.db.models import Q, F, Max, Count
from django.http import HttpResponse
from .models import Warning
from createdata.models import XmlData, EquipmentData
import json, copy


# 查询设备列表(监控屏，温湿度，ups)
def get_equipment(request):
    ip_str = request.GET.get('ip')
    """
    方法一：
    name_obj = Warning.objects.filter(warn_ip=ip_str)
    name_set = list(set([obj.warn_name for obj in name_obj]))
    print(name_set)
    """
    # 方法二
    # json_list = []
    name_queryset = Warning.objects.values('warn_name').distinct()
    json_list = [obj["warn_name"] for obj in name_queryset]
    # print(json_list)
    #  转换成json格式传送
    json_list = json.dumps(json_list)
    return JsonResponse(json_list, safe=False)


# 历史数据页面 对应的曲线图
def post_historydata(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6 版本以上不需要解码了
    request_data = json.loads(json_str)
    ip = request_data['ip']
    equipment = request_data['item']
    starttime = request_data['starttime']
    endtime = request_data['endtime']
    # print(equipment)
    # 得到一个区间列表
    print(ip)
    """
    1.通过equipment名称和日期区间，得到一个查询集对象
    2.把对象通过equipment_name字段分组 得到8个分组对象
    3.分别把8个分组对象，按日期进行去重
    4.合并数据
    """
    # 1.
    obj_data = EquipmentData.objects.filter(Q(equipment_ip=ip) &
                                            Q(equipment__contains=equipment) &
                                            Q(equipment_time__gt=starttime) &
                                            Q(equipment_time__lt=endtime))[:100]
    # print(len(obj_data))
    """  使用随机数 变得更加慢 """
    # sample = random.sample(range(obj_data.count()), 20)
    # obj_list = [obj_data.all()[i] for i in sample]

    # obj_list = obj_data.order_by('?')[:2]
    # print(obj_list)

    # 发送数据列表
    Eqdata_list = []
    for obj_eq in obj_data:
        # print(obj_eq)
        data = {}
        data["equipment"] = obj_eq.equipment
        data["name"] = obj_eq.equipment_name
        data["sigid"] = obj_eq.equipment_folat
        data["unit"] = obj_eq.equipment_unit
        data["float_data"] = obj_eq.equipment_text
        data["data_time"] = obj_eq.equipment_time
        Eqdata_list.append(data)

    # name_queryset = obj_list.values('equipment_name').distinct()
    # json_list = [obj["equipment_name"] for obj in name_queryset]
    # print(len(json_list))

    # for i in Eqdata_list:
    #     a = i["data_time"]
    #     i["data_time"] = re.match(r'^\S+', a).group()
    #     data_list = []
    #     # if i["name"] in json_list:
    #     #     data_list.append(i)

    return JsonResponse(Eqdata_list, safe=False)


# 历史告警
def post_historyalarm(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6 版本以上不需要解码了
    request_data = json.loads(json_str)
    ip = request_data['ip']
    equipment = request_data['item']
    starttime = request_data['starttime']
    endtime = request_data['endtime']
    warning_list = Warning.objects.filter(
        Q(warn_ip=ip) & Q(warn_name__contains=equipment) & Q(warn_time__gt=starttime) & Q(warn_time__lt=endtime))
    # 当值为 0 1变化时
    data_list = []
    start_time = []  # 所有的告警时间
    end_time = []  #
    flag = True
    # print(len(warning_list))
    # print(warning_list[len(warning_list) - 1].warn_data)
    for index, i in enumerate(warning_list):
        if flag and int(i.warn_data) == 0:
            pass
        if flag and int(i.warn_data) == 1:
            start_time.append(i.warn_time)
            flag = False
        if not flag and int(i.warn_data) == 0:
            end_time.append(i.warn_time)
            flag = True
        if index == (len(warning_list) - 1) and int(warning_list[len(warning_list) - 1].warn_data) == 1:
            end_time.append("Null")
    # print(start_time)
    # print(end_time)
    for index, item in enumerate(start_time):
        warn_obj = Warning.objects.filter(warn_time=item).first()
        data = {}
        data["equipment"] = warn_obj.warn_name
        data["information"] = warn_obj.warn_data
        data["unit"] = warn_obj.unit
        data["warn_level"] = warn_obj.warn_level
        data["warn_text"] = warn_obj.warn_text
        data["start_time"] = item
        data["end_time"] = end_time[index]
        data_list.append(data)

    return JsonResponse("ok", safe=False)

