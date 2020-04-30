


# import objgraph
# dict_list = objgraph.by_type('dict')
# def save_to_file(self, name, items):
#   with open(name, 'w') as outputs:
#     for idx, item in enumerate(items):
#       try:
#         outputs.write(str(idx) + " ### ")
#         outputs.write(str(item))
#         outputs.write('\n')
#       except Exception as e:
#         print(e)
#     outputs.flush()

'''
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
                    # 1. 通过遍历得到的ip 在站点表中查询对应的ip，得到站点对象。filter得到的是列表[]
                    site = divices.objects.filter(divice_ip=ip)[0]
                    # 2. 通过遍历constants常量中UPS_Signal的值。
                    for i in constants.UPS_Signal:
                        # 3. 通过ip得到唯一站点，通过信号id和名称得到指定的点位，通过last获取最新的一条数据。
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
'''

"""# 3、获取实时详细数据(ups 温湿度 空调)
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

"""
