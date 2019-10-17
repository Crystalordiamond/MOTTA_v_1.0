# -*- coding: utf-8 -*-
from xmldata.models import XmlData
from createdata.models import EquipmentData
from warning.models import Warning
from divices.models import divices
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import json
import time
from django.db.models import Q, F



# 告警实时数据
@accept_websocket
def echo(request):
    if not request.is_websocket():  # 如果不是socket链接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            print("普通的http方法")
            return HttpResponse(message)
        except:
            print("普通的http方法报错")
            return HttpResponse("普通的http方法报错")
    else:
        for message in request.websocket:
            # print(request.websocket)
            # print(message)
            # websockt传递的是二进制数据
            print("前端传过来的数据：%s" % message.decode())
            # 通过DataConfigTool收集 这些标准信息
            while True:
                list_data = []  # 严重告警列表
                list_data1 = []  # 一般告警列表
                # 获取模块的字典对象[{"监控屏IO":[{},{},{},...]},...,...]
                for item in list_war:
                    # 获取模块名称"equipment=监控屏IO"，及模块里面的设备列表value = [{"监控屏IO, 烟感": ["烟雾告警", "有告警", "严重告警", "-", 1]},{...},{...},...]
                    for equipment, value in item.items():
                        # 获得字典对象
                        # print(equipment)
                        for value_list in value:
                            # 获得告警设备和告警信息
                            for eq_name, alarm in value_list.items():
                                # print(alarm)
                                # ---------------------《 严重告警存入数据库 》----------------------
                                if alarm[2] == "严重告警" and eq_name == "温湿度, 温度":
                                    data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                    # 获取最新的ID 将其保存到全局变量“max1_id”，然后来做第二次对比判断
                                    # 防止将重复的数据存入告警表中，拿id做比对
                                    if alarm[5]["max_id"] != data.id:
                                        alarm[5]["max_id"] = data.id
                                        # 将告警存入数据库
                                        Warning.objects.create(
                                            warn_level=alarm[2],
                                            warn_text=alarm[0],
                                            warn_time=data.data_time,
                                            warn_name=equipment,
                                            warn_data=data.float_data,
                                            unit=alarm[3],
                                            is_delete=False,
                                            warn_ip=data.divice_ip,
                                            # 查询到对应站点（通过ip）
                                            equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                        )
                                    if alarm[5]["max_id"] == data.id:
                                        pass
                                    if data.float_data >= alarm[4]:
                                    # if data.float_data >= 20:
                                        # 告警站点
                                        divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                            values("divice_name")[0]["divice_name"]
                                        # 告警设备
                                        alarm_model = equipment
                                        # 告警名称
                                        alarm_divice = alarm[0]
                                        # 告警内容
                                        # print(type(data.float_data))
                                        # print(type(alarm[3]))
                                        alarm_data = str(data.float_data) + alarm[3]
                                        # 告警时间
                                        alarm_time = data.data_time
                                        # 告警等级
                                        alarm_level = alarm[2]
                                        # 传给前端的数据
                                        data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                     "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                     "alarm_time": alarm_time, "alarm_level": alarm_level}
                                        # 将每一条数据添加到列表
                                        list_data.append(data_dict)
                                # 判断
                                if alarm[2] == "严重告警" and eq_name != "温湿度, 温度":
                                    data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                    # 获取最新的ID 将其保存到全局变量“max1_id”，然后来做第二次对比判断
                                    if alarm[5]["max_id"] != data.id:
                                        alarm[5]["max_id"] = data.id
                                        Warning.objects.create(
                                            warn_level=alarm[2],
                                            warn_text=alarm[0],
                                            warn_time=data.data_time,
                                            warn_name=equipment,
                                            warn_data=data.float_data,
                                            unit=alarm[3],
                                            is_delete=False,
                                            warn_ip=data.divice_ip,
                                            # 查询到对应站点（通过ip）
                                            equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                        )
                                    if alarm[5]["max_id"] == data.id:
                                        pass
                                    if data.float_data != alarm[4]:
                                    # if data.float_data == alarm[4]:
                                        # 告警站点
                                        divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                            values("divice_name")[0]["divice_name"]
                                        # 告警设备
                                        alarm_model = equipment
                                        # 告警名称
                                        alarm_divice = alarm[0]
                                        # 告警内容
                                        alarm_data = alarm[1]
                                        # 告警时间
                                        alarm_time = data.data_time
                                        # 告警等级
                                        alarm_level = alarm[2]
                                        # 传给前端的数据
                                        data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                     "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                     "alarm_time": alarm_time, "alarm_level": alarm_level}
                                        # 将每一条数据添加到列表
                                        list_data.append(data_dict)

                                # ---------------------《一般告警存入数据库 》----------------------
                                if alarm[2] != "严重告警":
                                    if eq_name == "温湿度, 温度" and alarm[0] == "低温告警":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        # 获取最新的ID 将其保存到全局变量“max1_id”，然后来做第二次对比判断
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5]["max_id"] == data.id:
                                            pass
                                        if data.float_data <= alarm[4]:
                                        # if data.float_data <= 30:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = str(data.float_data) + alarm[3]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                                    if eq_name == "温湿度, 湿度" and alarm[0] == "高湿告警":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5].get("max_id") == data.id:
                                            pass
                                        if data.float_data >= alarm[4]:
                                        # if data.float_data >= 30:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = str(data.float_data) + alarm[3]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                                    if eq_name == "温湿度, 湿度" and alarm[0] == "低湿告警":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5].get("max_id") == data.id:
                                            pass
                                        if data.float_data <= alarm[4]:
                                        # if data.float_data <= 30:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = str(data.float_data) + alarm[3]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                                    if eq_name != "温湿度, 温度":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5].get("max_id") == data.id:
                                            pass
                                        if data.float_data != alarm[4]:
                                        # if data.float_data == alarm[4]:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = alarm[1]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                # ----------------------------------<存入历史数据>--------------------------------------
                store_historyData()
                # ----------------------------------<详情页面 实时更新数据 环境实时数据数据>--------------------------------------
                data_dict = {
                    # 环境
                    "AC_SAT": XmlData.objects.filter(name="空调, 送风温度").order_by("-id").first().float_data,
                    "AC_RAT": XmlData.objects.filter(name="空调, 吸气温度").order_by("-id").first().float_data,
                    "AC_RAH": XmlData.objects.filter(name="空调, 室内湿度").order_by("-id").first().float_data,
                    "AC_ST": "开" if int(
                        XmlData.objects.filter(name="空调, 设备通讯状态").order_by("-id").first().float_data) == 1 else "关",
                    # 电力
                    "PW_MV": XmlData.objects.filter(name="UPS, 输入电压").order_by("-id").first().float_data,
                    "PW_OV": XmlData.objects.filter(name="UPS, 输出电压").order_by("-id").first().float_data,
                    "PW_LR": XmlData.objects.filter(name="UPS, 输出负载率").order_by("-id").first().float_data,
                    "PW_BT": XmlData.objects.filter(name="UPS, 电池剩余时间").order_by("-id").first().float_data,
                    "PW_ROW": XmlData.objects.filter(name="主路电表, 功率").order_by("-id").first().float_data,
                    "PW_EC": XmlData.objects.filter(name="UPS, 输出功率因素").order_by("-id").first().float_data,
                    # 安防
                    "DR_ST": "开" if int(
                        XmlData.objects.filter(name="监控屏IO, 机柜门").order_by("-id").first().float_data) == 1 else "关",
                    # "DR_VD": XmlData.objects.filter(name="UPS, 输出功率因素").order_by("-id").first().float_data,
                    # 其他
                    "DR_MW": "无" if int(
                        XmlData.objects.filter(name="监控屏IO, 漏水").order_by("-id").first().float_data) == 1 else "有",
                    "DR_SD": "无" if int(
                        XmlData.objects.filter(name="监控屏IO, 烟感").order_by("-id").first().float_data) == 1 else "有",

                }
                # 将“严重告警”和“一般告警”发送前端
                data_dict = {"严重告警": list_data, "一般告警": list_data1, "data_dict": data_dict}
                # 转换成json格式传送
                str_list = json.dumps(data_dict)
                # print("返回给前端的数据", str_list)
                # 发送消息到客户端
                request.websocket.send(str_list.encode())
                list_data.clear()
                list_data1.clear()


# 用于展示历史数据(结合list_eq查询xmldata)
def store_historyData():
    for item in list_eq:
        # 获取模块名称"equipment=监控屏IO"，及模块里面的设备列表value = [{...},{...},{...},...]
        for equipment, value in item.items():
            # 获得字典对象
            # print(equipment)
            for value_list in value:
                # 获得告警设备和告警信息
                for eq_name, alarm in value_list.items():
                    # print(eq_name)
                    # print(alarm)
                    xmldata_obj = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                    # print(xmldata_obj[0])
                    # print(xmldata_obj.id)
                    if alarm[0]["max_id"] != xmldata_obj.id:
                        alarm[0]["max_id"] = xmldata_obj.id
                        # print(alarm[0]["max_id"])
                        # 先得到所有的key 然后判断float_data==key
                        key_list = list(alarm[0].keys())
                        # print(key_list)
                        # 遍历key_list 与取得的浮点数（转化后）相等，通过key取得对应的value
                        value_data = [alarm[0][key] for key in key_list if str(int(xmldata_obj.float_data)) == key]
                        # 判断value_data 为空则赋值null
                        value_data_lsit = value_data[0] if value_data != [] else str(xmldata_obj.float_data)
                        # print(value_data_lsit)
                        EquipmentData.objects.create(
                            # 设备
                            equipment=equipment,
                            # 设备名称
                            equipment_name=alarm[0]["name"],
                            # 信息值
                            equipment_folat=xmldata_obj.float_data,
                            # 内容根据信息值判断
                            equipment_text=value_data_lsit,
                            # 单位
                            equipment_unit=alarm[0]["unit"],
                            # 时间
                            equipment_time=xmldata_obj.data_time,
                            # 关联IP
                            equipment_ip=xmldata_obj.divice_ip,
                            # 外建
                            divices=divices.objects.get(divice_ip=xmldata_obj.divice_ip)

                        )
                    if alarm[0]["max_id"] == xmldata_obj.id:
                        pass
