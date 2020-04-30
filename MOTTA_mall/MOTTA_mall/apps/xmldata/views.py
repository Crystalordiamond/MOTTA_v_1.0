import copy
import datetime
from functools import reduce

from xmldata.models import XmlData
from .models import equipments, Signals_meaing, Events
from divices.models import divices
from rbac.models import User
from warning.models import AlarmContent, Warning, HistoryData
from dwebsocket.decorators import accept_websocket
from django.http import HttpResponse
import json, time
from django.db.models import Q

from celery_tasks.email.tasks import send_verify_mail
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from twilio.rest import Client
from . import constants

from django import db
import gc

gc.isenabled()

db.reset_queries()
list_ip = []  # 定义一个全局变量,用来接收http请求查询的ip
time_flg = datetime.datetime.now()  # 定义一个全局变量,接收时间字符串


# time_flg = "1990-09-09 09:09:09"  # 定义一个全局变量,接收时间字符串

# 0.将告警数据存入数据表
@accept_websocket
def websocket(request):
    # print(request.is_websocket())
    if request.is_websocket() == False:  # 如果不是socket链接
        global list_ip
        list_ip = []
        # 如果是普通的http方法
        data = request.body.decode()
        data_dicts = json.loads(data)
        # 1.获取前端传过来的用户名
        user = data_dicts['user']
        # 2.查询数据库获得用户关联的站点ip
        # print('ws的用户名称',user)
        ip_list = User.objects.filter(username=user)[0].divices_set.all()
        for i in ip_list:
            list_ip.append(i.divice_ip)
        return HttpResponse(json.dumps(list_ip))

    elif request.is_websocket() == True:
        print('# 0.将告警数据存入数据表：', list_ip)
        id_flg = None  # 设置最新数据的默认id，防止取到重复值
        while True:
            data = XmlData.objects.filter().last()
            if data and data.id != id_flg:
                id_flg = data.id
                # print(id_flg)
                # 确保ip有值
                if list_ip != []:
                    # 通过遍历ip池，通过ip查询
                    for ip in list_ip:
                        # 得到对应ip设备的最新一条信息
                        # data存在且 data.id不存在[判断data存在，新增了站点，没有实际数据的设备的情况]
                        if ip == data.divice_ip:
                            # 1、通过map表的equipid得到设备中间表的EquipId，然后得到EquipTemplateId
                            equipments_data = equipments.objects.filter(
                                Q(Equipment_ip=data.divice_ip) & Q(EquipId=data.equipid))
                            # 将浮点数转化为字符串
                            # print(id_flg)
                            # print(equipments_data)
                            a = '%.f' % data.float_data
                            """1.这里存入历史数据
                                历史数据存在Signals_meaing中，Signals_meaing表中有代表状态和事件的重复名称
                            """
                            history_data = HistoryData.objects.filter()
                            # print("-------------",history_data)
                            # 有重复值是因为id混淆
                            unit_data = Signals_meaing.objects.filter(Q(Signals_ip=data.divice_ip) & Q(
                                EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(SignalId=data.sigid))
                            db.close_old_connections()
                            """
                            查询Signals_meaing列表 同一个信号值会有多个值。
                            1.判断如果长度>1存在多个值需要比较
                            2.StateValue=None和Meaning=None这是唯一值
                            3.不理解查看Signals_meaing表结构
                            """
                            if unit_data.count() > 1:
                                # 这里得到的是有单位的数值，过滤掉了状态
                                unit_data = unit_data.filter(Q(StateValue=None) & Q(Meaning=None))
                                db.close_old_connections()
                                # for i in unit_data:
                                #     print(i.Meaning)
                                #     print(i.StateValue)
                                #     print(type(i.Meaning))
                                # print("===============", len(unit_data))
                            if history_data.count() > 0:
                                # print("===============", len(unit_data), unit_data[0].Unit)
                                # 1.判断存入的数据是否存在(ip,设备id 179,参数名称)
                                his_data = HistoryData.objects.filter(equipment_ip=ip).filter(
                                    equipment_other=equipments_data[0].EquipTemplateId).filter(
                                    equipment_parameter=unit_data[0].SignalName)
                                db.close_old_connections()
                                if his_data.count() > 0:
                                    # print(len(his_data))
                                    #  todo 一分钟存储一次
                                    history_time = datetime.timedelta(days=1 / 24 / 60)
                                    # 取最新的一条数据判断 存入数据是并发存入，有可能时间字段是一样的所以筛选ip。
                                    history_list = his_data.last().equipment_time
                                    history_new = datetime.datetime.strptime(data.data_time, "%Y-%m-%d %H:%M:%S")
                                    history_old = datetime.datetime.strptime(history_list, "%Y-%m-%d %H:%M:%S")
                                    if history_new - history_old > history_time:
                                        HistoryData.objects.create(
                                            equipment_site=divices.objects.filter(divice_ip=data.divice_ip)[
                                                0].divice_site,
                                            equipment_equipment=equipments_data[0].EquipmentName,
                                            equipment_parameter=unit_data[0].SignalName,
                                            equipment_value=a,
                                            equipment_unit='-' if unit_data[0].Unit == '' else unit_data[0].Unit,
                                            equipment_time=data.data_time,
                                            equipment_ip=data.divice_ip,
                                            equipment_other=equipments_data[0].EquipTemplateId,
                                        )
                                    db.close_old_connections()
                                else:
                                    # print(len(his_data))
                                    HistoryData.objects.create(
                                        equipment_site=divices.objects.filter(divice_ip=data.divice_ip)[
                                            0].divice_site,
                                        equipment_equipment=equipments_data[0].EquipmentName,
                                        equipment_parameter=unit_data[0].SignalName,
                                        equipment_value=a,
                                        equipment_unit='-' if unit_data[0].Unit == '' else unit_data[0].Unit,
                                        equipment_time=data.data_time,
                                        equipment_ip=data.divice_ip,
                                        equipment_other=equipments_data[0].EquipTemplateId,
                                    )
                                db.close_old_connections()
                            else:
                                HistoryData.objects.create(
                                    equipment_site=divices.objects.filter(divice_ip=data.divice_ip)[0].divice_site,
                                    equipment_equipment=equipments_data[0].EquipmentName,
                                    equipment_parameter=unit_data[0].SignalName,
                                    equipment_value=a,
                                    equipment_unit='-' if unit_data[0].Unit == '' else unit_data[0].Unit,
                                    equipment_time=data.data_time,
                                    equipment_ip=data.divice_ip,
                                    equipment_other=equipments_data[0].EquipTemplateId
                                )
                            db.close_old_connections()
                            # 2、根据xmldata里面的sigid值来查找，注意 不是所有的sigid值都有对应的数据 这是告警数据 event会有除了ConditionId不同的重复值
                            """
                            查询Events列表 同一个信号值会有多个值。
                            1.判断如果长度>1存在多个值需要比较
                            2.ConditionId=None和 Meaning=None这是唯一值
                            3.不理解查看Events表结构
                            """
                            evn_data = Events.objects.filter(
                                Q(Events_ip=data.divice_ip) & Q(EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(
                                    EventId=data.sigid))
                            db.close_old_connections()
                            if evn_data.count() != 0:
                                # 1个event信号有多个值
                                for evn in evn_data:
                                    # print("=======================")
                                    # print(evn.Meaning)
                                    # 必须要有告警信息(过滤掉重复值)
                                    if evn.Meaning != None:
                                        # manage_list将用户列表转化成字符串，传给前端
                                        manage_list = []
                                        for i in divices.objects.filter(divice_ip=data.divice_ip)[0].user_id.all():
                                            manage_list.append(i.username)
                                        # 告警的等级
                                        if evn.EventSeverity == '3':
                                            war_level = 'Critical'
                                        elif evn.EventSeverity == '2':
                                            war_level = 'General'
                                        else:
                                            war_level = 'Msg'
                                        # 创建好字典数据后面复用
                                        data_dict = {
                                            'location': divices.objects.filter(divice_ip=data.divice_ip)[
                                                0].divice_location,
                                            # 告警的站点位置
                                            'site': divices.objects.filter(divice_ip=data.divice_ip)[0].divice_site,
                                            # 告警的站点
                                            'alarm': evn.EventName,  # 告警的名称
                                            'alarm_text': evn.Meaning,  # 告警的内容
                                            'equipment': equipments_data[0].EquipmentName,  # 告警的设备
                                            'level': war_level,  # 告警等级
                                            'manage': ','.join(manage_list),
                                            # 该站点关联的用户
                                            'lssue_time': data.data_time,  # 告警时间
                                            'alarm_id': evn.EventId,  # 告警的ID
                                            'alarm_ip': data.divice_ip,  # 告警的IP
                                            'EquipTemplateId': evn.EquipTemplateId,  # EquipTemplateId

                                            'value': a,  # 告警的值
                                            'unit': '-' if unit_data[0].Unit == '' else unit_data[0].Unit,  # 告警的单位
                                            "StartCompareValue": evn.StartCompareValue
                                        }
                                        b = evn.StartCompareValue
                                        c = evn.StartOperation
                                        if c == "=":
                                            c = "=="
                                        # print('%s %s %s' % (a, c, b))
                                        # 3、eval() 函数用来执行一个字符串表达式，并返回表达式的值。表达式的值返回True则为告警
                                        """实时告警列表"""
                                        if eval('%s %s %s' % (a, c, b)) == True:
                                            alarm_data = AlarmContent.objects.filter(Q(alarm_ip=data.divice_ip) & Q(
                                                EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(
                                                alarm_id=data.sigid) & Q(equipment=equipments_data[0].EquipmentName))
                                            if alarm_data.count() > 0:
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
                                                    StartCompareValue=data_dict['StartCompareValue'],
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
                                                    StartCompareValue=data_dict['StartCompareValue'],
                                                    alarm_flag='1',
                                                )
                                            """历史告警列表"""
                                            win_data = Warning.objects.filter(warn_ip=ip).filter(
                                                warn_other=equipments_data[0].EquipTemplateId).filter(
                                                warn_parameter=unit_data[0].SignalName)
                                            if win_data.count() > 0:
                                                # print(len(win_data))
                                                # todo 一小时存入一次
                                                time_data = datetime.timedelta(days=1 / 24 / 60)
                                                # 获取最新的一条数据的时间
                                                time_list = win_data.last().warn_time
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
                                                        warn_other=equipments_data[0].EquipTemplateId,
                                                    )
                                                else:
                                                    pass
                                            # 满足告警条件 新数据直接创建
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
                                                    warn_other=equipments_data[0].EquipTemplateId,
                                                )
                                        # 表达式的值返回False则为非告警
                                        elif eval('%s %s %s' % (a, c, b)) == False:
                                            alarm_data2 = AlarmContent.objects.filter(
                                                Q(alarm_ip=data.divice_ip) & Q(
                                                    EquipTemplateId=equipments_data[0].EquipTemplateId) & Q(
                                                    alarm_id=data.sigid) & Q(
                                                    equipment=equipments_data[0].EquipmentName))
                                            if alarm_data2.count() != 0:
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
                                                    StartCompareValue=data_dict['StartCompareValue'],
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
                                                    StartCompareValue=data_dict['StartCompareValue'],
                                                    alarm_flag='0',
                                                )
                                        db.close_old_connections()
                                        del data_dict

                                    else:
                                        pass
                                    db.close_old_connections()
                        else:
                            pass
                        db.close_old_connections()
                else:
                    print("该用户没有关联的ip设备")
                db.close_old_connections()
            else:
                pass
            db.close_old_connections()


# 1.将实时告警 展示给前端
@accept_websocket
def QueryWebsocket(request):
    if request.is_websocket() == True:
        WebSocket = request.websocket
        print("# 1.将数据实时展示给前端")
        while True:
            # 用户关联的站点来展示告警
            if list_ip:
                alarm_list = []  # 每个ip对应的 告警列表
                """
                实时告警列表
                1、先查询10001  连接状态，如果未连接直接报未连接错误，无需报里面详细告警
                2、查询到的查询集有值
                2、连接 则根据equipment名称 查询下面的子告警
                """
                for i in list_ip:
                    alarm_id = AlarmContent.objects.filter(Q(alarm_ip=i) & Q(alarm_id='10001'))
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
                if len(alarm_list) != 0:
                    # 1.去重
                    run_function = lambda x, y: x if y in x else x + [y]
                    alarm_list = reduce(run_function, [[], ] + alarm_list)
                    # 1.1 去掉Msg提示的告警
                    for item in alarm_list[::-1]:
                        if item['level'] == 'Msg':
                            alarm_list.remove(item)
                        # print(alarm_list)
                    # 2.获取当前时间
                    now_times = datetime.datetime.now()
                    # 3.发送告警邮件
                    send_mails(list_ip, alarm_list, now_times)
                    # 4.将数据传给前端
                    alarm_data_str = {"main": alarm_list}
                    json_data = json.dumps(alarm_data_str)  # 将得到的列表数据转换成json数据
                    WebSocket.send(json_data.encode('utf-8'))  # 编码成utf-8传给前端
                    time.sleep(2)


"""
1.不同协议的MDC，通过ip做区分。
2.MDC内有不同的设备，相同设备端口不一样（232,485），相同设备地址不一样（485，地址改为1 改为2）。
3.设备有多个点位的情况（大电表，小电表）。 特殊情况（三相可能是三个单相相加 或者就一个大电表）
"""


# 2. vtu-io, ups 电表 温湿度 空调 实时数据
@accept_websocket
def GetWebsocket(request):
    if request.is_websocket() == True:
        WebSocket = request.websocket
        print("# 2.ups 电表 温湿度 空调")
        while True:
            if list_ip:
                data_list = []  # 每个ip对应的 告警列表
                """
                ups的协议同，对应的信号点也会不同，需要建一个不同协议对应不同的数值池
                """
                # 2、确保取到的值没有重复的，在区分ip
                for ip in list_ip:
                    # 1. 通ip过滤，equipment。filter得到的是列表[] （后面会用到）
                    site = divices.objects.filter(divice_ip=ip)[0]
                    # 2. 获取ups的数据 根据ip查寻equipment表得到ups数量。
                    # 2.1 得到所有的equipmen设备对象
                    LibName = equipments.objects.filter(Equipment_ip=ip)
                    # 2.2 根据ups的so名称过滤，得到ups对象(ups的so文件名称，为常量，需要手动添加)
                    # 一些ip的MDC没有ups则为空列表
                    ups_list = [i for i in LibName if i.LibName in constants.ups_type]
                    # 2.3 根据不同的协议类型做比较 "UPS_6-10K.so", "UPS_INVT_X7-20.so", "UPS-GXT4.so"
                    for j in ups_list:
                        # 2.3.1 如果ups是UPS_6-10K.so
                        if j.LibName == "UPS_6-10K.so":
                            # 2.3.2 有多个ups情况下 (模板是通用的 区别在于equipment表的EquipmentName名称不同,需要拼接字符串)
                            # 这里需要深拷贝字典对象，不然修改的是原始字典，下一次循环的时候，会一直累加。
                            RYY_co = copy.deepcopy(constants.RYY)
                            for k in RYY_co:
                                # 2.3.3 拼接字符串
                                k['name'] = j.EquipmentName + ', ' + k['name']
                            # 2.3.4 通过ip得到唯一站点，通过信号id和名称得到指定的点位，通过last获取最新的一条数据。
                            for index, i in enumerate(RYY_co):
                                data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                    name=i.get("name")).last()
                                # 2.3.5 如果data有值，将值返回给前端
                                if data:
                                    data_dict = {
                                        "name": "UPS",
                                        "site_name": j.EquipmentName,
                                        "singnal_name": constants.RYY[index]["name"],
                                        "singnal_data": data.float_data,
                                        "singnal_site": site.divice_site if site else '',
                                        "singnal_time": data.data_time,
                                        "site_type": j.LibName
                                    }
                                    data_list.append(data_dict)
                        # 2.3.2 如果ups是UPS_INVT_X7-20.so(目前是瑞尔时代监控)
                        if j.LibName == "UPS_INVT_X7-20.so":
                            pass
                        # 2.3.3 如果ups是UPS-GXT4.so
                        if j.LibName == "UPS_GXT4.so":
                            VERTIV_co = copy.deepcopy(constants.VERTIV)
                            for k in VERTIV_co:
                                # 2.3.3 拼接字符串
                                k['name'] = j.EquipmentName + ', ' + k['name']
                            # 2.3.4 通过ip得到唯一站点，通过信号id和名称得到指定的点位，通过last获取最新的一条数据。
                            for index, i in enumerate(VERTIV_co):
                                data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                    name=i.get("name")).last()
                                # 2.3.5 如果data有值，将值返回给前端
                                if data:
                                    data_dict = {
                                        "name": "UPS",
                                        "site_name": j.EquipmentName,
                                        "singnal_name": constants.VERTIV[index]["name"],
                                        "singnal_data": data.float_data,
                                        "singnal_site": site.divice_site if site else '',
                                        "singnal_time": data.data_time,
                                        "site_type": j.LibName
                                    }
                                    data_list.append(data_dict)
                    """ 3.1 根据温湿度so文件名称，获得温湿度的对象。"""
                    temp_list = [i for i in LibName if i.LibName in constants.TH_type]
                    for k in temp_list:
                        # 3.2 有多个温湿度情况下 (模板是通用的 区别在于equipment表的EquipmentName名称不同,需要拼接字符串)
                        # 这里需要深拷贝字典对象，不然修改的是原始字典，下一次循环的时候，会一直累加。
                        TH_co = copy.deepcopy(constants.TempsHumidity)
                        # 3.3 这里在拼接名称时候，xmldata在存储数据时，因为xml模板特殊字符串，是做了修改的
                        for l in TH_co:
                            # 2.3.3 拼接字符串,replace()替换指定字符串
                            l['name'] = k.EquipmentName.replace('&', '-') + ', ' + l['name']
                        for index, i in enumerate(TH_co):
                            data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                name=i.get("name")).last()
                            # 2.3.5 如果data有值，将值返回给前端
                            if data:
                                data_dict = {
                                    "name": "TH",
                                    "site_name": k.EquipmentName,
                                    "singnal_name": constants.TempsHumidity[index]["name"],
                                    "singnal_data": data.float_data,
                                    "singnal_site": site.divice_site if site else '',
                                    "singnal_time": data.data_time,
                                    "site_type": "THSE10.so"
                                }
                                data_list.append(data_dict)

                    """4.1 电表so文件名称，获得电表对象"""
                    meter_list = [i for i in LibName if i.LibName in constants.Meter_type]
                    # 4.2 根据不同的协议类型做比较 "YD2010C-K-V.so", "DDS3366D-1P.so"
                    for m in meter_list:
                        # 4.2.1 如果电表是YD2010C-K-V.so大电表
                        if m.LibName == "YD2010C-K-V.so":
                            # 4.2.2 有多个电表情况下 (模板是通用的 区别在于equipment表的EquipmentName名称不同,需要拼接字符串)
                            # 这里需要深拷贝字典对象，不然修改的是原始字典，下一次循环的时候，会一直累加。(大电表)
                            B_meter_co = copy.deepcopy(constants.B_meter)
                            for n in B_meter_co:
                                # 4.2.3 拼接字符串
                                if n['name'].find("&#xA;&#xA;") != -1:
                                    n['name'] = m.EquipmentName + ', ' + n['name'].replace('&#xA;&#xA;', '')
                                    # print(n['name'])
                                else:
                                    n['name'] = m.EquipmentName + ', ' + n['name']
                            # 4.2.4 通过ip得到唯一站点，通过信号id和名称得到指定的点位，通过last获取最新的一条数据。
                            for index, i in enumerate(B_meter_co):
                                data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                    name=i.get("name")).last()
                                # 4.2.5 如果data有值，将值返回给前端
                                if data:
                                    data_dict = {
                                        "name": "Meter",
                                        "site_name": m.EquipmentName,
                                        "singnal_name": constants.B_meter[index]["name"],
                                        "singnal_data": data.float_data,
                                        "singnal_site": site.divice_site if site else '',
                                        "singnal_time": data.data_time,
                                        "site_type": m.LibName
                                    }
                                    data_list.append(data_dict)
                        # 4.3 如果电表是DDS3366D-1P.so小电表
                        if m.LibName == "DDS3366D-1P.so":
                            # 4.3.1 有多个电表情况下 (模板是通用的 区别在于equipment表的EquipmentName名称不同,需要拼接字符串)
                            # 这里需要深拷贝字典对象，不然修改的是原始字典，下一次循环的时候，会一直累加。(大电表)
                            L_meter_co = copy.deepcopy(constants.L_meter)
                            for n in L_meter_co:
                                # 4.2.3 拼接字符串
                                n['name'] = m.EquipmentName + ', ' + n['name']
                            # 4.2.4 通过ip得到唯一站点，通过信号id和名称得到指定的点位，通过last获取最新的一条数据。
                            for index, i in enumerate(L_meter_co):
                                data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                    name=i.get("name")).last()
                                # 4.2.5 如果data有值，将值返回给前端
                                if data:
                                    data_dict = {
                                        "name": "Meter",
                                        "site_name": m.EquipmentName,
                                        "singnal_name": constants.L_meter[index]["name"],
                                        "singnal_data": data.float_data,
                                        "singnal_site": site.divice_site if site else '',
                                        "singnal_time": data.data_time,
                                        "site_type": m.LibName
                                    }
                                    data_list.append(data_dict)

                    """5.1 空调so文件名称，获得空调对象"""

                    AC_list = [i for i in LibName if i.LibName in constants.AC_type]
                    for k in AC_list:
                        # 如果空调是卡乐控制器
                        if k.LibName == "SmoothAir_Carel_DX.so":
                            # 5.2 有多个空调情况下 (模板是通用的 区别在于equipment表的EquipmentName名称不同,需要拼接字符串)
                            # 这里需要深拷贝字典对象，不然修改的是原始字典，下一次循环的时候，会一直累加。
                            AC_co = copy.deepcopy(constants.AC_KL)
                            # 5.3 这里在拼接名称时候，xmldata在存储数据时，因为xml模板特殊字符串，是做了修改的
                            for l in AC_co:
                                # 2.3.3 拼接字符串,replace()替换指定字符串
                                l['name'] = k.EquipmentName + ', ' + l['name']
                            for index, i in enumerate(AC_co):
                                data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                    name=i.get("name")).last()
                                # 2.3.5 如果data有值，将值返回给前端
                                if data:
                                    data_dict = {
                                        "name": "AC",
                                        "site_name": k.EquipmentName,
                                        "singnal_name": constants.AC_KL[index]["name"],
                                        "singnal_data": data.float_data,
                                        "singnal_site": site.divice_site if site else '',
                                        "singnal_time": data.data_time,
                                        "site_type": k.LibName
                                    }
                                    data_list.append(data_dict)
                        # 如果空调是深蓝控制器
                        if k.LibName == "SL1600F_FC.so":
                            # 5.2 有多个空调情况下 (模板是通用的 区别在于equipment表的EquipmentName名称不同,需要拼接字符串)
                            # 这里需要深拷贝字典对象，不然修改的是原始字典，下一次循环的时候，会一直累加。
                            AC_co = copy.deepcopy(constants.AC_SL)
                            # 5.3 这里在拼接名称时候，xmldata在存储数据时，因为xml模板特殊字符串，是做了修改的
                            for l in AC_co:
                                # 2.3.3 拼接字符串,replace()替换指定字符串
                                l['name'] = k.EquipmentName + ', ' + l['name']
                            for index, i in enumerate(AC_co):
                                data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                    name=i.get("name")).last()
                                # 2.3.5 如果data有值，将值返回给前端
                                if data:
                                    data_dict = {
                                        "name": "AC",
                                        "site_name": k.EquipmentName,
                                        "singnal_name": constants.AC_SL[index]["name"],
                                        "singnal_data": data.float_data,
                                        "singnal_site": site.divice_site if site else '',
                                        "singnal_time": data.data_time,
                                        "site_type": k.LibName
                                    }
                                    data_list.append(data_dict)
                    """6.1 vtu so文件名称，获得vtu对象"""
                    vtu_list = [i for i in LibName if i.LibName in constants.VTU_type]
                    for x in vtu_list:
                        # 5.2 有多个空调情况下 (模板是通用的 区别在于equipment表的EquipmentName名称不同,需要拼接字符串)
                        # 这里需要深拷贝字典对象，不然修改的是原始字典，下一次循环的时候，会一直累加。
                        VTU_co = copy.deepcopy(constants.VTU)
                        # 5.3 这里在拼接名称时候，xmldata在存储数据时，因为xml模板特殊字符串，是做了修改的
                        for y in VTU_co:
                            # 2.3.3 拼接字符串,replace()替换指定字符串
                            y['name'] = x.EquipmentName + ', ' + y['name']
                        for index, i in enumerate(VTU_co):
                            data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                                name=i.get("name")).last()
                            # 2.3.5 如果data有值，将值返回给前端
                            if data:
                                data_dict = {
                                    "name": "VTU",
                                    "site_name": x.EquipmentName,
                                    "singnal_name": constants.VTU[index]["name"],
                                    "singnal_data": data.float_data,
                                    "singnal_site": site.divice_site if site else '',
                                    "singnal_time": data.data_time,
                                    "site_type": "VTUIO.so"
                                }
                                data_list.append(data_dict)
                if len(data_list) != 0:
                    # print(len(data_list))
                    data_list_str = {"details": data_list}
                    json_data = json.dumps(data_list_str)  # 将得到的列表数据转换成json数据
                    WebSocket.send(json_data.encode('utf-8'))  # 编码成utf-8传给前端
                    # time.sleep(2)


"""
得到所有设备的详情信息，并是每一条都是最新的，实时更新
1.通过ip，可到对应站点所有的设备对象equipmets表，其中EquipID和EquipmentName（注意特殊字符）都是唯一的，可以作为标识。
2.得到设备所有的signal，然后对SignalName去重即可得到每个设备的状态信息表(在筛选时候需要加一个标识，设备协议相同，是共用一个模板的)
3.Signal表是全部的设备信息，如何区别不同的设备，通过EquipTemplateId这个唯一标识，然后给signal的名称做字符串拼接。通过拼接的字符串找打xmldata最新的一条数据
4.遍历这个信息表，在Xmldata表中获取最新的数据
5.将数据返回给前端
"""


# 3、获取实时详细数据(ups 温湿度 空调)
@accept_websocket
def PostWebsocket(request):
    if request.is_websocket() == True:
        WebSocket = request.websocket
        print("# 3、获取实时详细数据")
        while True:
            if list_ip:
                data_list = []  # 每个ip对应的 告警列表
                for ip in list_ip:
                    # 1.0 得到单个站点的设备列表
                    equipment_ob = equipments.objects.filter(Equipment_ip=ip)
                    # 2.0 在signal表中同一个signalname有statevalue和meaning组合字段是唯一的，可以用这个2个字段去重
                    # 2.1 通过ip删选得到当前站点的signal表 通过StateValue和Meaning字段筛选
                    signal_meaning = Signals_meaing.objects.filter(Signals_ip=ip).filter(Q(StateValue=None) & Q(Meaning=None))
                    # 2.2 通过EquipTemplateId来区分每一台设备
                    for i in equipment_ob:
                        for j in signal_meaning:
                            # 2.3 在遍历signal表时候 如果和i的EquipTemplateId相同，则拼接字符串查询最新的数据
                            if i.EquipTemplateId == j.EquipTemplateId:
                                # 2.4 拼接字符串的特殊情况Temp&Humidity需要替换&，这是在存数据时候，对特殊字符串进行了处理的
                                # 如果字符串找不到返回的是int -1
                                if i.EquipmentName.find('&') != -1:
                                    str_name = i.EquipmentName.replace('&', '-') + ', ' + j.SignalName
                                    xml_data = XmlData.objects.filter(divice_ip=ip).filter(name=str_name).last()
                                    if xml_data:
                                        data_dict = {
                                            "equipment": i.EquipmentName,
                                            "parameter": j.SignalName,
                                            "value": xml_data.float_data,
                                            "Unit": j.Unit,
                                            "ip": ip,
                                            "time": xml_data.data_time,
                                            "site": divices.objects.filter(divice_ip=ip)[0].divice_site
                                        }
                                        data_list.append(data_dict)
                                else:
                                    # print(i.EquipmentName)
                                    str_name = i.EquipmentName + ', ' + j.SignalName
                                    xml_data = XmlData.objects.filter(divice_ip=ip).filter(name=str_name).last()
                                    if xml_data:
                                        data_dict = {
                                            "equipment": i.EquipmentName,
                                            "parameter": j.SignalName,
                                            "value": xml_data.float_data,
                                            "Unit": j.Unit,
                                            "ip": ip,
                                            "time": xml_data.data_time,
                                            "site": divices.objects.filter(divice_ip=ip)[0].divice_site
                                        }
                                        data_list.append(data_dict)
                if len(data_list) != 0:
                    # print(len(data_list))
                    # print(data_list)
                    data_list_str = {"details_data": data_list}
                    json_data = json.dumps(data_list_str)  # 将得到的列表数据转换成json数据
                    WebSocket.send(json_data.encode('utf-8'))  # 编码成utf-8传给前端
                    # print(len(data_list))
                    # time.sleep(2)


# 定时发送邮件
def send_mails(list_ip, alarm_list, now_time):
    global time_flg
    # todo 10分钟发送一次邮件
    if now_time - time_flg > datetime.timedelta(days=1 / 24 / 6):
        time_flg = now_time
        # 1.收件人
        to_email = []
        # to_phone = []
        for ip in list_ip:
            user = divices.objects.filter(divice_ip=ip)[0].user_id.all()
            for i in user:
                to_email.append(i.email)
                # to_phone.append('+86' + i.u_phone)
        # 2.给收件人列表去重
        to_email = list(set(to_email))
        # 3.整理列表格式
        # 3.1 获取模板
        print("to_email", to_email)
        template = loader.get_template('index.html')
        context = {"alarm_list": alarm_list}
        html_msg = template.render(context)
        # subject = "邮件告警"
        send_verify_mail.delay(to_email, html_msg)
        # send_mail(subject, "", settings.EMAIL_HOST_USER, to_email, html_message=html_msg)
        print("邮件发送成功,发送时间%s", (now_time - time_flg))
        # 4.发送短信告警
        # 4.1.给电话列表去重
        # to_phone = list(set(to_phone))
        # 4.2.配置发送的信息
        # account_sid = "AC29bee85a3bb88c1f1c2511ec09911ad3"
        # auth_token = "cbc23860e7c6664cfa247473123de75a"
        # client = Client(account_sid, auth_token)
        # 4.3 给短信拼接信息
        # sms_list = []
        # for index, i in enumerate(alarm_list):
        #     sms_list.append(
        #         str(index) + ": " + i["site"] + " in " + i["location"] + " had a " + i["equipment"] + " " + i[
        #             "alarm"] + " " + i["alarm_text"] + ", " + " alarm time was " + i["lssue_time"] + ".")
        # # 4.4 将列表拼接成字符串
        # sms_list = ";".join(sms_list)
        # print(sms_list)
        # 4.4 发送短信 测试只能给注册的手机号使用
        # client.messages.create(
        #     to="+8613651416330",
        #     # from_="+12029183862",
        #     body=sms_list)
        # print("短信发送成功")

    else:
        pass
