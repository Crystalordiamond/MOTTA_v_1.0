import time

from django.http.response import JsonResponse
from django.db.models import Q, F, Max, Count
from django.http import HttpResponse
from .models import Warning, HistoryData
from rbac.models import User
from xmldata.models import XmlData, equipments
import json, copy
from functools import reduce


# 0、查询现有站点的 site equipment parameter alarm level 列表
def get_equipment(request):
    json_str = request.body
    json_str = json_str.decode()
    request_data = json.loads(json_str)
    # 获取equipment
    equipment_list = []
    for i in equipments.objects.filter(Equipment_ip__in=request_data["ip"]):
        data_dict = {
            "equipment": i.EquipmentName
        }
        equipment_list.append(data_dict)
    # 对equipment_list去重
    run_function = lambda x, y: x if y in x else x + [y]
    a = reduce(run_function, [[], ] + equipment_list)

    """distinct()方法是同一列去重"""
    data_dict = {
        "site": [{"site": i.divice_site} for i in
                 User.objects.filter(username=request_data["user"])[0].divices_set.all()],
        "equipment": a,
        "parameter": [{"parameter": i['warn_parameter']} for i in
                      Warning.objects.filter(warn_ip__in=request_data["ip"]).values('warn_parameter').distinct()],
        "level": [{"level": i['warn_level']} for i in Warning.objects.values('warn_level').distinct()],
        # 这个是给历史数据列表使用的  parameter
        "history_parameter": [{"parameter": i['equipment_parameter']} for i in
                              HistoryData.objects.filter(equipment_ip__in=request_data["ip"]).values(
                                  'equipment_parameter').distinct()],
    }
    #  转换成json格式传送
    json_list = json.dumps(data_dict)
    # print("json_list: ", len(json_list))
    return JsonResponse(json_list, safe=False)


# 1、历史告警
def post_historyalarm(request):
    json_str = request.body
    json_str = json_str.decode()
    request_data = json.loads(json_str)
    if len(request_data) == 1:
        # print("len(request_data) == 1", request_data)
        data = Warning.objects.filter(warn_site=request_data["site"])
        data_list = []
        for i in data:
            data_dict = {
                "equipment": i.warn_equipment
            }
            data_list.append(data_dict)
        # 去重
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)
    elif len(request_data) == 2:
        # print("len(request_data) == 2", request_data)
        data = Warning.objects.filter(warn_site=request_data["site"]).filter(
            warn_equipment=request_data["equipment"])
        data_list = []
        for i in data:
            data_dict = {
                "parameter": i.warn_parameter
            }
            data_list.append(data_dict)
        # 去重
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)
    else:
        # print(request_data)
        # 此处的equipment和site在数据库中位置调换了
        site = request_data['site']
        equipment = request_data['equipment']
        parameter = request_data['parameter']
        level = request_data['level']
        start_time = time.strptime(request_data['start_time'], "%Y-%m-%d %H:%M:%S")
        end_time = time.strptime(request_data['end_time'], "%Y-%m-%d %H:%M:%S")
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_time)
        warning_list = Warning.objects.filter(
            Q(warn_site=site) & Q(warn_equipment=equipment) & Q(warn_parameter=parameter) & Q(warn_level=level) & Q(
                warn_time__gt=start_time) & Q(warn_time__lt=end_time))
        # print(warning_list)
        data_list = []
        for item in warning_list:
            data_dict = {
                "site": item.warn_site,
                "equipment": item.warn_equipment,
                "parameter": item.warn_parameter,
                "alarm": item.warn_alarm,
                "value": item.warn_value,
                "unit": item.warn_unit,
                "level": item.warn_level,
                "time": item.warn_time,
            }
            data_list.append(data_dict)
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)


# 2、历史数据页面
def post_historydata(request):
    json_str = request.body
    json_str = json_str.decode()
    request_data = json.loads(json_str)
    # print(request_data)
    if len(request_data) == 1:
        data = HistoryData.objects.filter(equipment_site=request_data["site"])
        data_list = []
        for i in data:
            data_dict = {
                "equipment": i.equipment_equipment
            }
            data_list.append(data_dict)
        # 去重
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)
    elif len(request_data) == 2:
        data = HistoryData.objects.filter(equipment_site=request_data["site"]).filter(
            equipment_equipment=request_data["equipment"])
        data_list = []
        for i in data:
            data_dict = {
                "parameter": i.equipment_parameter
            }
            data_list.append(data_dict)
        # 去重
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)
    else:
        site = request_data['site']
        equipment = request_data['equipment']
        parameter = request_data['parameter']
        start_time = time.strptime(request_data['start_time'], "%Y-%m-%d %H:%M:%S")
        end_time = time.strptime(request_data['end_time'], "%Y-%m-%d %H:%M:%S")
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_time)

        data = HistoryData.objects.filter(
            Q(equipment_site=site) & Q(equipment_equipment=equipment) & Q(equipment_parameter=parameter) & Q(
                equipment_time__gt=start_time) & Q(
                equipment_time__lt=end_time))
        # print(data)
        data_list = []
        for item in data:
            data_dict = {
                "site": item.equipment_site,
                "equipment": item.equipment_equipment,
                "parameter": item.equipment_parameter,
                "value": item.equipment_value,
                "unit": item.equipment_unit,
                "time": item.equipment_time,
            }
            data_list.append(data_dict)
        # print(data_list)
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)


# 3、历史数据图表展示
def signaldata(request):
    json_str = request.body
    json_str = json_str.decode()
    request_data = json.loads(json_str)
    # 1.0 这里判断传过来参数长度，作用在于逐递搜索，当用户传递第一个site设备参数，返回设备名称（用户选择使用）
    if len(request_data) == 1:
        # print("len(request_data) == 1", request_data)
        data = HistoryData.objects.filter(equipment_site=request_data["site"])
        data_list = []
        for i in data:
            data_dict = {
                "equipment": i.equipment_equipment
            }
            data_list.append(data_dict)
        # 去重
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)
    # 2.0 当参数长度为2时，说明有了站点和设备，需要得到parameter参数（用户选择使用）
    elif len(request_data) == 2:
        # print("len(request_data) == 2", request_data)
        data = HistoryData.objects.filter(equipment_site=request_data["site"]).filter(
            equipment_equipment=request_data["equipment"])
        data_list = []
        for i in data:
            data_dict = {
                "parameter": i.equipment_parameter
            }
            data_list.append(data_dict)
        # 去重
        run_function = lambda x, y: x if y in x else x + [y]
        a = reduce(run_function, [[], ] + data_list)
        return JsonResponse(a, safe=False)
    # 3.0 其他情况，当用户一个参数都没有填写，或者至少有3+2(时间参数)个参数（用户查询使用）
    else:
        """
        time_data = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        data_time = time.strptime('2019-1-1 23:8:0','%Y-%m-%d %H:%M:%S')
        print("将时间转化为格式化字符串:",time_data)
        print("将字符串转化为时间类型:",data_time)
        """
        # 将前端的字符串时间格式，转化为时间类型
        start_time = time.strptime(request_data['start_time'], "%Y-%m-%d %H:%M:%S")
        end_time = time.strptime(request_data['end_time'], "%Y-%m-%d %H:%M:%S")
        # 将时间类型 转为格式化字符串
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_time)

        data1 = HistoryData.objects.filter(
            Q(equipment_site=request_data["site1"]) & Q(equipment_equipment=request_data["equipment1"]) & Q(
                equipment_parameter=request_data["parameter1"]) & Q(
                equipment_time__gt=start_time) & Q(
                equipment_time__lt=end_time))
        data2 = HistoryData.objects.filter(
            Q(equipment_site=request_data["site2"]) & Q(equipment_equipment=request_data["equipment2"]) & Q(
                equipment_parameter=request_data["parameter2"]) & Q(
                equipment_time__gt=start_time) & Q(
                equipment_time__lt=end_time))
        data3 = HistoryData.objects.filter(
            Q(equipment_site=request_data["site3"]) & Q(equipment_equipment=request_data["equipment3"]) & Q(
                equipment_parameter=request_data["parameter3"]) & Q(
                equipment_time__gt=start_time) & Q(
                equipment_time__lt=end_time))
        data4 = HistoryData.objects.filter(
            Q(equipment_site=request_data["site4"]) & Q(equipment_equipment=request_data["equipment4"]) & Q(
                equipment_parameter=request_data["parameter4"]) & Q(
                equipment_time__gt=start_time) & Q(
                equipment_time__lt=end_time))
        data_time = HistoryData.objects.filter(
            Q(equipment_time__gt=start_time) & Q(equipment_time__lt=end_time))
        data_list = []
        data_list2 = []
        data_list3 = []
        data_list4 = []
        time_list = []
        for item in data1:
            data_dict = {
                "site": item.equipment_site,
                "equipment": item.equipment_equipment,
                "parameter": item.equipment_parameter,
                "value": item.equipment_value,
                "unit": item.equipment_unit,
                "time": item.equipment_time,
            }
            data_list.append(data_dict)
        for item in data2:
            data_dict = {
                "site": item.equipment_site,
                "equipment": item.equipment_equipment,
                "parameter": item.equipment_parameter,
                "value": item.equipment_value,
                "unit": item.equipment_unit,
                "time": item.equipment_time,
            }
            data_list2.append(data_dict)
        for item in data3:
            data_dict = {
                "site": item.equipment_site,
                "equipment": item.equipment_equipment,
                "parameter": item.equipment_parameter,
                "value": item.equipment_value,
                "unit": item.equipment_unit,
                "time": item.equipment_time,
            }
            data_list3.append(data_dict)
        for item in data4:
            data_dict = {
                "site": item.equipment_site,
                "equipment": item.equipment_equipment,
                "parameter": item.equipment_parameter,
                "value": item.equipment_value,
                "unit": item.equipment_unit,
                "time": item.equipment_time,
            }
            data_list4.append(data_dict)
        for item in data_time:
            data_dict = {
                "time": item.equipment_time,
            }
            time_list.append(data_dict)
        # 给时间字段去重
        run_function = lambda x, y: x if y in x else x + [y]
        data_list = reduce(run_function, [[], ] + data_list)
        data_list2 = reduce(run_function, [[], ] + data_list2)
        data_list3 = reduce(run_function, [[], ] + data_list3)
        data_list4 = reduce(run_function, [[], ] + data_list4)
        data_dicts = {
            "signal1": data_list,
            "signal2": data_list2,
            "signal3": data_list3,
            "signal4": data_list4,
        }
        data_dicts = json.dumps(data_dicts)
        print("data_dicts:", data_dicts)

        return JsonResponse(data_dicts, safe=False)
