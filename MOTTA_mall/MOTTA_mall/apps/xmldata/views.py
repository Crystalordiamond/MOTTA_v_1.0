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





# 1.将数据实时展示给前端
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


# 2.ups 电表 温湿度 空调
@accept_websocket
def GetWebsocket(request):
    if request.is_websocket() == True:
        WebSocket = request.websocket
        print("# 2.ups 电表 温湿度 空调")
        # id_flg = None  # 先取值 后比较，如果后面不匹配会把最新数据过滤掉  这里立id——flg会导致死循环，循环ip导致每次的flg都会不一样
        while True:
            # 用户关联的站点来展示告警
            if list_ip:
                data_list = []  # 每个ip对应的 告警列表
                """
                ups的协议同，对应的信号点也会不同，需要建一个不同协议对应不同的数值池
                """
                # 1.获取最新的一条数据  不区分ip
                # # data = XmlData.objects.filter().last()
                # if data and id_flg != data.id:
                #     id_flg = data.id
                # 2、确保取到的值没有重复的，在区分ip
                for ip in list_ip:
                    site = divices.objects.filter(divice_ip=ip)[0]
                    for i in constants.UPS_Signal:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "UPS_Signal",
                                "UPS_Signal": data.float_data,
                                "site": site.divice_site if site else '',
                                "time": data.data_time
                            }
                            data_list.append(data_dict)
                            # print(data_dict)
                    for i in constants.temps:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "temps",
                                "temps": data.float_data,
                                "site": site.divice_site if site else '',
                                "time": data.data_time
                            }
                            data_list.append(data_dict)
                    for i in constants.Humidity:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "Humidity",
                                "Humidity": data.float_data,
                                "site": site.divice_site if site else '',
                                "time": data.data_time
                            }
                            data_list.append(data_dict)
                    for i in constants.input_vol:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "input_vol",
                                "input_vol": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.output_vol:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "output_vol",
                                "output_vol": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.input_fre:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "input_fre",
                                "input_fre": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.output_fre:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "output_fre",
                                "output_fre": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.input_phase:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "input_phase",
                                "input_phase": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.output_phase:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "output_phase",
                                "output_phase": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.meter_power:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "meter_power",
                                "meter_power": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.ups_load:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "ups_load",
                                "ups_load": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.Return_Temp:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "Return_Temp",
                                "Return_Temp": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                            # print(data_dict)
                    for i in constants.Discharge_Temp:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "Discharge_Temp",
                                "Discharge_Temp": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.AC_Humidity:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "AC_Humidity",
                                "AC_Humidity": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)
                    for i in constants.AC_Mode:
                        # 1.得到最新的一条数据
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        if data:
                            # 2.通过equipid来查询equipment表中的equipID
                            EquipId = equipments.objects.filter(Equipment_ip=ip).filter(EquipId=data.equipid).last()
                            # 3.得到value对应meaning (meaning有很多)
                            meanings = Signals_meaing.objects.filter(EquipTemplateId=EquipId.EquipTemplateId).filter(
                                Signals_ip=ip).filter(SignalId=i.get("sigid"))
                            a = '%.f' % data.float_data
                            for i in meanings:
                                if i.StateValue == a:
                                    # print(i.Meaning)
                                    data_dict = {
                                        "name": "AC_Mode",
                                        "AC_Mode": data.float_data,
                                        "meaning": i.Meaning,
                                        "site": site.divice_site if site else ''
                                    }
                                    data_list.append(data_dict)
                                else:
                                    pass
                    for i in constants.Leaking:
                        data = XmlData.objects.filter(divice_ip=ip).filter(sigid=i.get("sigid")).filter(
                            name=i.get("name")).last()
                        # if data and data.id != id_flg:
                        #     id_flg = data.id
                        if data:
                            data_dict = {
                                "name": "Leaking",
                                "Leaking": data.float_data,
                                "site": site.divice_site if site else ''
                            }
                            data_list.append(data_dict)

                if len(data_list) != 0:
                    # print(data_list)
                    data_list_str = {"details": data_list}
                    json_data = json.dumps(data_list_str)  # 将得到的列表数据转换成json数据
                    WebSocket.send(json_data.encode('utf-8'))  # 编码成utf-8传给前端
                    # time.sleep(2)


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
                    ups_id = equipments.objects.filter(Equipment_ip=ip).filter(EquipmentName="UPS")
                    temp_id = equipments.objects.filter(Equipment_ip=ip).filter(EquipmentName="Temp&Humidity")
                    ac_id = equipments.objects.filter(Equipment_ip=ip).filter(EquipmentName="Air Conditioner")
                    site = divices.objects.filter(divice_ip=ip)[0].divice_site
                    if ups_id.count() != 0:
                        # 1.获取信号表里面 ip和设备id的数据表
                        data = Signals_meaing.objects.filter(Signals_ip=ip).filter(
                            EquipTemplateId=ups_id[0].EquipTemplateId)
                        # 2.继续过滤 Unit | StateValue | Meaning 不为空的值
                        # data = data.filter(~Q(Unit="") & ~Q(StateValue="") & ~Q(Meaning=""))  # 为啥不行
                        data = data.exclude(Q(Unit="") & Q(StateValue=None) & Q(Meaning=None))
                        for signal in data:
                            # print(signal.Unit, signal.StateValue, signal.Meaning)
                            # print(ups_id[0].EquipId)
                            # 1.得到所有关联ip的关联ups设备id的数据，也就是所有的ups数据
                            xml_data = XmlData.objects.filter(divice_ip=ip).filter(equipid=ups_id[0].EquipId)
                            # 2.根据信号的id得到信号的批量数据,再得到最新的一条数据
                            xml_data_value = xml_data.filter(sigid=signal.SignalId).last()
                            # 3.如果signal的StateValue为空则是没有事件的，直接获取值。有值需要比对获取meaning
                            # print(xml_data_value)
                            a = '%.f' % xml_data_value.float_data
                            # print(type(a))
                            if signal.StateValue == None:
                                data_dict = {
                                    "equipment": "UPS",
                                    "parameter": signal.SignalName,
                                    "value": xml_data_value.float_data,
                                    "Unit": signal.Unit,
                                    "meaning": signal.Meaning,
                                    "time": xml_data_value.data_time,
                                    "site": site
                                }
                                data_list.append(data_dict)
                            elif signal.StateValue == a:
                                data_dict = {
                                    "equipment": "UPS",
                                    "parameter": signal.SignalName,
                                    "value": xml_data_value.float_data,
                                    "Unit": signal.Unit,
                                    "meaning": signal.Meaning,
                                    "time": xml_data_value.data_time,
                                    "site": site
                                }
                                data_list.append(data_dict)
                    if temp_id.count() != 0:
                        data = Signals_meaing.objects.filter(Signals_ip=ip).filter(
                            EquipTemplateId=temp_id[0].EquipTemplateId)
                        # 继续过滤 Unit | StateValue | Meaning 不为空
                        # data = data.filter(~Q(Unit="") & ~Q(StateValue="") & ~Q(Meaning=""))  # 为啥不行
                        data = data.exclude(Q(Unit="") & Q(StateValue=None) & Q(Meaning=None))
                        # print(len(data))
                        for signal in data:
                            # print(signal.Unit, signal.StateValue, signal.Meaning)
                            # print(ups_id[0].EquipId)
                            # 1.得到所有关联ip的关联ups设备id的数据，也就是所有的ups数据
                            xml_data = XmlData.objects.filter(divice_ip=ip).filter(equipid=temp_id[0].EquipId)
                            # 2.根据信号的id得到信号的批量数据,再得到最新的一条数据
                            xml_data_value = xml_data.filter(sigid=signal.SignalId).last()
                            # print(xml_data_value)
                            # 3.如果signal的StateValue为空则是没有事件的，直接获取值。有值需要比对获取meaning
                            # print(type(signal.StateValue))
                            # if xml_data_value:  # todo 这个温湿度状态 为啥会存在None的情况  temp_id写错了
                            a = '%.f' % xml_data_value.float_data
                            # print(type(a))
                            # print(a)
                            if signal.StateValue == None:
                                data_dict = {
                                    "equipment": "Temp&Humidity",
                                    "parameter": signal.SignalName,
                                    "value": xml_data_value.float_data,
                                    "Unit": signal.Unit,
                                    "meaning": signal.Meaning,
                                    "time": xml_data_value.data_time,
                                    "site": site
                                }
                                data_list.append(data_dict)
                            elif signal.StateValue == a:
                                data_dict = {
                                    "equipment": "Temp&Humidity",
                                    "parameter": signal.SignalName,
                                    "value": xml_data_value.float_data,
                                    "Unit": signal.Unit,
                                    "meaning": signal.Meaning,
                                    "time": xml_data_value.data_time,
                                    "site": site
                                }
                                data_list.append(data_dict)
                    if ac_id.count() != 0:
                        data = Signals_meaing.objects.filter(Signals_ip=ip).filter(
                            EquipTemplateId=ac_id[0].EquipTemplateId)
                        # 继续过滤 Unit | StateValue | Meaning 不为空
                        # data = data.filter(~Q(Unit="") & ~Q(StateValue="") & ~Q(Meaning=""))  # 为啥不行
                        data = data.exclude(Q(Unit="") & Q(StateValue=None) & Q(Meaning=None))
                        # print(len(data))
                        for signal in data:
                            # print(ups_id[0].EquipId)
                            # 1.得到所有关联ip的关联ups设备id的数据，也就是所有的ups数据
                            xml_data = XmlData.objects.filter(divice_ip=ip).filter(equipid=ac_id[0].EquipId)
                            # 2.根据信号的id得到信号的批量数据,再得到最新的一条数据
                            xml_data_value = xml_data.filter(sigid=signal.SignalId).last()
                            # 3.如果signal的StateValue为空则是没有事件的，直接获取值。有值需要比对获取meaning
                            # print(type(signal.StateValue))
                            # print(signal.StateValue)
                            if xml_data_value:
                                a = '%.f' % xml_data_value.float_data
                                # print(type(a))
                                # print(a)
                                if signal.StateValue == None:
                                    data_dict = {
                                        "equipment": "Air Conditioner",
                                        "parameter": signal.SignalName,
                                        "value": xml_data_value.float_data,
                                        "Unit": signal.Unit,
                                        "meaning": signal.Meaning,
                                        "time": xml_data_value.data_time,
                                        "site": site
                                    }
                                    data_list.append(data_dict)
                                elif signal.StateValue == a:
                                    data_dict = {
                                        "equipment": "Air Conditioner",
                                        "parameter": signal.SignalName,
                                        "value": xml_data_value.float_data,
                                        "Unit": signal.Unit,
                                        "meaning": signal.Meaning,
                                        "time": xml_data_value.data_time,
                                        "site": site
                                    }
                                    data_list.append(data_dict)
                                    # print(data_dict)
                if len(data_list) != 0:
                    # print(len(data_list))
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
