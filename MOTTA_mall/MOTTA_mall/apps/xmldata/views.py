import datetime

from xmldata.models import XmlData
from .models import equipments, Signals_meaing, Events
from divices.models import divices
from rbac.models import User
from warning.models import AlarmContent, Warning, HistoryData
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import json, time
from django.db.models import Q, F

list_ip = []  # 定义一个全局变量,用来接收http请求查询的ip


# 将告警数据存入数据表
@accept_websocket
def websocket(request):
    # print(request.is_websocket())
    if request.is_websocket() == False:  # 如果不是socket链接
        global list_ip
        list_ip = []
        # 如果是普通的http方法
        data = request.body.decode()
        data_dict = json.loads(data)
        # 1.获取前端传过来的用户名
        user = data_dict['user']
        # 2.查询数据库获得用户关联的站点ip
        # print('ws的用户名称',user)
        ip_list = User.objects.filter(username=user)[0].divices_set.all()
        for i in ip_list:
            list_ip.append(i.divice_ip)
        return HttpResponse(json.dumps(list_ip))

    elif request.is_websocket() == True:
        print('通过http请求获取的ip列表：', list_ip)
        ip_flag = None  # 设置最新数据的默认id，防止取到重复值
        while True:
            # 确保ip有值
            if list_ip != []:
                # 通过遍历ip池，通过ip查询
                for ip in list_ip:
                    # 得到对应ip设备的最新一条信息
                    data = XmlData.objects.filter(divice_ip=ip).last()
                    # data存在且 data.id不存在[判断data存在，新增了站点，没有实际数据的设备的情况]
                    if data and data.id != ip_flag:
                        ip_flag = data.id
                        # 1、通过map表的equipid得到设备中间表的EquipId，然后得到EquipTemplateId
                        equipments_data = equipments.objects.filter(
                            Q(Equipment_ip=data.divice_ip) & Q(EquipId=data.equipid))
                        # 将浮点数转化为字符串
                        a = '%.f' % data.float_data

                        """这里存入历史数据"""
                        history_data = HistoryData.objects.first()
                        unit_data = Signals_meaing.objects.filter(Q(Signals_ip=data.divice_ip) & Q(
                            EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(SignalId=data.sigid))[
                            0]
                        if history_data:
                            history_data_time = HistoryData.objects.filter(equipment_time=data.data_time)
                            if history_data_time.count() == 0:
                                # 一分钟存储一次
                                history_data = datetime.timedelta(days=1 / 24 / 60)
                                # 取最新的一条数据判断
                                history_list = HistoryData.objects.all().last().equipment_time

                                history_new = datetime.datetime.strptime(data.data_time, "%Y-%m-%d %H:%M:%S")
                                history_old = datetime.datetime.strptime(history_list, "%Y-%m-%d %H:%M:%S")
                                if history_new - history_old > history_data:
                                    HistoryData.objects.create(
                                        equipment_site=divices.objects.filter(divice_ip=data.divice_ip)[0].divice_site,
                                        equipment_equipment=equipments_data[0].EquipmentName,
                                        equipment_parameter=unit_data.SignalName,
                                        equipment_value=a,
                                        equipment_unit='-' if unit_data.Unit == '' else unit_data.Unit,
                                        equipment_time=data.data_time,
                                        equipment_ip=data.divice_ip,

                                    )
                        else:
                            HistoryData.objects.create(
                                equipment_site=divices.objects.filter(divice_ip=data.divice_ip)[0].divice_site,
                                equipment_equipment=equipments_data[0].EquipmentName,
                                equipment_parameter=unit_data.SignalName,
                                equipment_value=a,
                                equipment_unit='-' if unit_data.Unit == '' else unit_data.Unit,
                                equipment_time=data.data_time,
                                equipment_ip=data.divice_ip
                            )
                        """"""
                        # 2、根据xmldata里面的sigid值来查找，注意 不是所有的sigid值都有对应的数据 这是告警数据 event会有除了ConditionId不同的重复值
                        evn_data = Events.objects.filter(
                            Q(Events_ip=data.divice_ip) & Q(EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(
                                EventId=data.sigid))
                        if evn_data.count() != 0:
                            # 1个event信号有多个值
                            for evn in evn_data:
                                # print(evn.Meaning)
                                # 必须要有告警信息
                                if evn.Meaning:
                                    data_dict = {
                                        'location': divices.objects.filter(divice_ip=data.divice_ip)[0].divice_location,
                                        # 告警的站点位置
                                        'site': divices.objects.filter(divice_ip=data.divice_ip)[0].divice_site,
                                        # 告警的站点
                                        'alarm': evn.EventName,  # 告警的名称
                                        'alarm_text': evn.Meaning,  # 告警的内容
                                        'equipment': equipments_data[0].EquipmentName,  # 告警的设备
                                        'level': 'Critical' if evn.EventSeverity == '3' else 'General',  # 告警等级
                                        'manage': [i.username for i in
                                                   divices.objects.filter(divice_ip=data.divice_ip)[0].user_id.all()],
                                        # 该站点关联的用户
                                        'lssue_time': data.data_time,  # 告警时间
                                        'alarm_id': evn.EventId,  # 告警的ID
                                        'alarm_ip': data.divice_ip,  # 告警的IP
                                        'EquipTemplateId': evn.EquipTemplateId,  # EquipTemplateId

                                        'value': a,  # 告警的值
                                        'unit': '-' if unit_data.Unit == '' else unit_data.Unit,  # 告警的单位
                                    }
                                    b = evn.StartCompareValue
                                    c = evn.StartOperation
                                    if c == "=":
                                        c = "=="
                                    # print('%s %s %s' % (a, c, b))
                                    # 3、eval() 函数用来执行一个字符串表达式，并返回表达式的值。表达式的值返回True则为告警
                                    """实时告警列表"""
                                    # 这里已经达成告警的条件了。 要保证时间是唯一的，不然时间字段会重复有多个。这是是遍历操作，不用考虑其他设备的重复。
                                    time_str = AlarmContent.objects.filter(lssue_time=data.data_time)
                                    if time_str.count() == 0:
                                        if eval('%s %s %s' % (a, c, b)) == True:
                                            alarm_data = AlarmContent.objects.filter(Q(alarm_ip=data.divice_ip) & Q(
                                                EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(
                                                alarm_id=data.sigid) & Q(equipment=equipments_data[0].EquipmentName))
                                            # if alarm_data.count() > 1:
                                            #     print("alarm_data值大于2了")
                                            #     break
                                            # print("alarm_data的值", alarm_data)
                                            # print("alarm_data的值", alarm_data.count())

                                            if alarm_data.count() != 0:
                                                if alarm_data.count() > 1:
                                                    print("alarm_data大于1了啊")
                                                    for i in alarm_data:
                                                        print(i.alarm_ip, i.EquipTemplateId, i.alarm_id, i.equipment)
                                                alarm_data.update(
                                                    site=data_dict['site'],
                                                    alarm=data_dict['alarm'],
                                                    alarm_text=data_dict['alarm_text'],
                                                    equipment=data_dict['equipment'],
                                                    level=data_dict['level'],
                                                    manage=data_dict['manage'],
                                                    lssue_time=data_dict['lssue_time'],
                                                    alarm_id=data_dict['alarm_id'],
                                                    alarm_ip=data_dict['alarm_ip'],
                                                    EquipTemplateId=data_dict['EquipTemplateId'],
                                                    alarm_flag='1',  # 告警唯一标识 告警为1 非告警为0
                                                )
                                            else:
                                                AlarmContent.objects.create(
                                                    site=data_dict['site'],
                                                    alarm=data_dict['alarm'],
                                                    alarm_text=data_dict['alarm_text'],
                                                    equipment=data_dict['equipment'],
                                                    level=data_dict['level'],
                                                    manage=data_dict['manage'],
                                                    lssue_time=data_dict['lssue_time'],
                                                    alarm_id=data_dict['alarm_id'],
                                                    alarm_ip=data_dict['alarm_ip'],
                                                    EquipTemplateId=data_dict['EquipTemplateId'],
                                                    alarm_flag='1',
                                                )
                                        # 表达式的值返回False则为非告警
                                        if eval('%s %s %s' % (a, c, b)) == False:
                                            # alarm_data2 = AlarmContent.objects.filter(
                                            #     Q(alarm_ip=evn.Events_ip) & Q(alarm_id=evn.EventId) & Q(
                                            #         equipment=equipments_data[0].EquipmentName))
                                            alarm_data2 = AlarmContent.objects.filter(Q(alarm_ip=data.divice_ip) & Q(
                                                EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(
                                                alarm_id=data.sigid) & Q(equipment=equipments_data[0].EquipmentName))
                                            # if alarm_data2.count() > 1:
                                            #     print(alarm_data2)
                                            #     print("alarm_data2值大于2了")
                                            #     break
                                            # print("alarm_data2的值", alarm_data2)
                                            # print("alarm_data2的值", alarm_data2.count())
                                            if alarm_data2.count() != 0:
                                                if alarm_data2.count() > 1:
                                                    print("alarm_data2大于1了啊")
                                                    for i in alarm_data2:
                                                        print(i.alarm_ip, i.EquipTemplateId, i.alarm_id, i.equipment)
                                                alarm_data2.update(
                                                    site=data_dict['site'],
                                                    alarm=data_dict['alarm'],
                                                    alarm_text=data_dict['alarm_text'],
                                                    equipment=data_dict['equipment'],
                                                    level=data_dict['level'],
                                                    manage=data_dict['manage'],
                                                    lssue_time=data_dict['lssue_time'],
                                                    alarm_id=data_dict['alarm_id'],
                                                    alarm_ip=data_dict['alarm_ip'],
                                                    EquipTemplateId=data_dict['EquipTemplateId'],
                                                    alarm_flag='0',
                                                )
                                            else:
                                                AlarmContent.objects.create(
                                                    site=data_dict['site'],
                                                    alarm=data_dict['alarm'],
                                                    alarm_text=data_dict['alarm_text'],
                                                    equipment=data_dict['equipment'],
                                                    level=data_dict['level'],
                                                    manage=data_dict['manage'],
                                                    lssue_time=data_dict['lssue_time'],
                                                    alarm_id=data_dict['alarm_id'],
                                                    alarm_ip=data_dict['alarm_ip'],
                                                    EquipTemplateId=data_dict['EquipTemplateId'],
                                                    alarm_flag='0',
                                                )
                                    else:
                                        pass
                                    """历史告警列表"""
                                    if Warning.objects.first():
                                        # 一分钟存储一次
                                        warn_data_time = Warning.objects.filter(warn_time=data.data_time)
                                        if warn_data_time.count() == 0:
                                            time_data = datetime.timedelta(days=1 / 24 / 60)
                                            # 获取最新的一条数据的时间
                                            time_list = Warning.objects.all().last().warn_time
                                            time_new = datetime.datetime.strptime(data_dict["lssue_time"],
                                                                                  "%Y-%m-%d %H:%M:%S")
                                            time_old = datetime.datetime.strptime(time_list, "%Y-%m-%d %H:%M:%S")
                                            if time_new - time_old > time_data:
                                                Warning.objects.create(
                                                    warn_site=data_dict["site"],
                                                    warn_equipment=data_dict["equipment"],
                                                    warn_parameter=data_dict["alarm"],  # 告警参数也是告警名称
                                                    warn_alarm=data_dict["alarm_text"],  # 告警内容
                                                    warn_value=data_dict["value"],
                                                    warn_unit=data_dict["unit"],
                                                    warn_level=data_dict["level"],
                                                    warn_time=data_dict["lssue_time"],
                                                    warn_ip=data_dict["alarm_ip"],
                                                )
                                    else:
                                        Warning.objects.create(
                                            warn_site=data_dict["site"],
                                            warn_equipment=data_dict["equipment"],
                                            warn_parameter=data_dict["alarm"],  # 告警参数也是告警名称
                                            warn_alarm=data_dict["alarm_text"],  # 告警内容
                                            warn_value=data_dict["value"],
                                            warn_unit=data_dict["unit"],
                                            warn_level=data_dict["level"],
                                            warn_time=data_dict["lssue_time"],
                                            warn_ip=data_dict["alarm_ip"],
                                        )


# 将数据实时展示给前端
@accept_websocket
def QueryWebsocket(request):
    if request.is_websocket() == True:
        WebSocket = request.websocket
        while True:
            # 用户关联的站点来展示告警
            if list_ip:
                alarm_list = []  # 每个ip对应的 告警列表
                for i in list_ip:
                    alarm_id = AlarmContent.objects.filter(Q(alarm_ip=i) & Q(alarm_id='10001'))
                    """
                    1、先查询10001  连接状态，如果未连接直接报未连接错误，无需报里面详细告警
                    2、查询到的查询集有值
                    2、连接 则根据equipment名称 查询下面的子告警
                    """
                    if alarm_id:
                        # print(alarm_id)
                        for j in alarm_id:
                            # print(j.alarm_id)
                            # 1、连接状态==1有告警，通信未连接
                            if j.alarm_flag == '1':
                                data_dict = {
                                    "site": divices.objects.filter(divice_ip=i).first().divice_site,
                                    "alarm": j.alarm,
                                    "alarm_text": j.alarm_text,
                                    "equipment": j.equipment,
                                    "level": j.level,
                                    "manage": j.manage,  # 该站点关联的用户  #ip地址关联的管理员
                                    "lssue_time": j.lssue_time,
                                    "location": divices.objects.filter(divice_ip=i).first().divice_location,
                                    # 查询alarm_flag=‘1’为True则该ip地址对应的站点有告警 为False则该站点无告警
                                    "status": 'Warning' if AlarmContent.objects.filter(alarm_flag='1') else 'Nomal',
                                    "alarm_ip": j.alarm_ip,
                                }
                                alarm_list.append(data_dict)
                            # 2、通信已经连接，查询子告警
                            elif j.alarm_flag == "0":
                                # 2.1 、查询10001 无告警下的其他子告警
                                data = AlarmContent.objects.filter(
                                    Q(alarm_ip=i) & Q(alarm_flag='1') & Q(equipment=j.equipment))
                                if data:
                                    # print(data)
                                    for k in data:
                                        data_dict = {
                                            "site": divices.objects.filter(divice_ip=i).first().divice_site,
                                            "alarm": k.alarm,
                                            "alarm_text": k.alarm_text,
                                            "equipment": k.equipment,
                                            "level": k.level,
                                            "manage": k.manage,  # 该站点关联的用户  #ip地址关联的管理员
                                            "lssue_time": k.lssue_time,
                                            "location": divices.objects.filter(divice_ip=i).first().divice_location,
                                            # 查询alarm_flag=‘1’为True则该ip地址对应的站点有告警 为False则该站点无告警
                                            "status": 'Warning' if AlarmContent.objects.filter(
                                                alarm_flag='1') else 'Nomal',
                                            "alarm_ip": k.alarm_ip,
                                        }
                                        alarm_list.append(data_dict)
                # print(len(alarm_list))
                json_data = json.dumps(alarm_list)  # 将得到的列表数据转换成json数据
                WebSocket.send(json_data.encode('utf-8'))  # 编码成utf-8传给前端
                time.sleep(2)


"""
从xmldata表中获取数据，将告警和未告警添加一个唯一标示，存到表中
温湿度数值注意
实时更新表，传给前端。
"""
