import copy
from ftplib import FTP
from xml.dom import minidom
# from pyModbusTCP.pyModbusTCP.client import ModbusClient
from pyModbusTCP.client import ModbusClient
import threading
import struct
import os, time, datetime
from pymysql import connect


class Ftp_Data(object):
    """
    用来获取xml文件和替换需要更改的文件
    """

    def __init__(self, ip):
        self.host = ip
        self.port = 2121
        self.username = "ftp"
        self.password = "ftp"
        self.localpath = "./"
        self.modbus_xml = "/data/mgrid/sampler/modbus_map.xml"
        self.XmlCfg_ftp_path = "/data/mgrid/sampler/XmlCfg"

        self.__old_str = "&"
        self.__new_str = "-"

        # self.__client = ModbusClient(host=self.host, port=502)
        self.__client = ModbusClient(host=self.host, port=502, debug=True)
        self.modbus_map_list = []  # 存储modbus_map_list表数据[{},{},{}...]
        self.MonitorUnitVTU = []  # 存储MonitorUnitVTU表数据[{},{},{}...]

        self.__conn = connect(host='localhost', port=3306, database="MOTTA_data", user="root", password="mysql",
                              charset="utf8")
        self.__cur = self.__conn.cursor()

        self.__address = 0
        self.__register = 1
        self.i = 0

        self.ftp = None  # 设置self.ftp=None的时候 ftp才能自动重新连接上

    def ftp_connect(self):
        """ 连接ftp """
        # 实例化FTP对象

        self.ftp = FTP()
        # ftp.set_debuglevel(2) 1        #打开调试级别2，显示详细信息
        try:
            self.ftp.connect(self.host, self.port)  # 连接
        except:
            raise IOError("%s ftp connect failed!" % self.host)
        try:
            self.ftp.login(self.username, self.password)  # 登录，如果匿名登录则用空串代替即可
        except:
            raise IOError("%s ftp login failed!" % self.host)
        else:
            print("%s FTP connection successful......" % self.host)

    def download_file(self):
        # 连接ftp()
        self.ftp_connect()
        """
        1.下载modbus_map.xml文件
        """
        # print(self.host)
        # exists()判断当前路径 是否有self.host文件夹
        if os.path.exists(os.path.join(self.localpath, self.host)):
            # 清空文件夹里面的数据及删除之前数据

            for i in os.listdir(os.path.join(self.localpath, self.host)):
                os.remove(os.path.join(self.localpath, self.host, i))
                # print("....移除文件%s" % i)
            params = self.host
            sql_list = []
            sql_list.append('''delete from tb_port where port_ip=%s;''')
            sql_list.append('''delete from tb_equipments where Equipment_ip=%s;''')
            sql_list.append('''delete from tb_logactions where logactions_ip=%s;''')
            sql_list.append('''delete from tb_Events where Events_ip=%s;''')
            sql_list.append('''delete from tb_Commands where Commands_ip=%s;''')
            sql_list.append('''delete from tb_Signals_meaing where Signals_ip=%s;''')
            sql_list.append('''delete from tb_xmldata where divice_ip=%s;''')
            for i in sql_list:
                # print(i)
                self.__cur.execute(i, params)
                self.__conn.commit()
            print("%s:文件夹已经存在" % self.host)

        else:
            # 创建当前文件
            os.mkdir(os.path.join(self.localpath, self.host))
        # 下载文件
        bufsize = 1024  # 设置缓冲块大小
        # 以写模式在本地打开文件
        fp = open(os.path.join(self.localpath, self.host, "modbus_map.xml"), 'wb')
        # 接收服务器上文件并写入本地打开的文件
        self.ftp.retrbinary('RETR ' + self.modbus_xml, fp.write, bufsize)
        # ftp.set_debuglevel(0)  # 关闭调试
        fp.close()  # 关闭文件
        print("-------------------------%sModbus_map.xml download completes-------------------------" % self.host)
        """
        2.批量下载XmlCfg中xml文件
        """
        file_list = self.ftp.nlst(self.XmlCfg_ftp_path)  # 获取下载的文件目录
        # print("批量下载XmlCfg中xml文件",file_list)
        files_list = []
        # 过滤非.xml文件结尾的文件
        for i in file_list:
            # 匹配以.xml结尾的文件名称
            if i.endswith('.xml') == True:
                files_list.append(i)
        bufsize = 1024 * 1024
        # print("-------------------------Start the download-------------------------")
        # print(files_list)
        for i in files_list:
            # 以写模式在本地打开文件
            fp = open(os.path.join(self.localpath, self.host, i), 'wb')
            # 接收服务器上文件并写入本地打开的文件
            self.ftp.retrbinary('RETR ' + self.XmlCfg_ftp_path + '/' + i, fp.write, bufsize)
            # ftp.set_debuglevel(0)  # 关闭调试
            # print("文件%s下载完成" % i)
        print("-------------------------批量下载%s:XmlCfg中xml文件成功-------------------------" % self.host)

    # 替换modbus_map.xml中的特殊字符
    def replace_str(self):
        """
        1、获取远程xml文档，到本地
        2、打开读取本地xml文件，修改字符串，保存到变量
        3、打开本地同名的xml文件，然后讲变量保存的值 写入到文档
        """
        self.download_file()
        # 将xml文件中的&替换成-    XML文件有五个不允许出现的特殊字符
        file_data = ""
        with open(os.path.join(self.localpath, self.host, "modbus_map.xml"), "r", encoding="utf-8") as f:
            # 遍历的每一行
            for line in f:
                if self.__old_str in line:
                    # Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
                    line = line.replace(self.__old_str, self.__new_str)
                file_data += line
        # print(file_data)
        with open(os.path.join(self.localpath, self.host, "modbus_map.xml"), "w", encoding="utf-8") as f:
            f.write(file_data)
        print("%s:modbus_map.xml中特殊字符替换完成!" % self.host)

    # 批量替换特殊字符&#xA;
    def replaces_str(self):
        xml_list = os.listdir(os.path.join(self.localpath, self.host))
        for xml in xml_list:
            file_data = ""
            with open(os.path.join(self.localpath, self.host, xml), "r", encoding="utf-8") as f:
                # 遍历的每一行
                for line in f:
                    if "&#xA;" in line:
                        # Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
                        line = line.replace("&#xA;", "")
                    file_data += line
            # print(file_data)
            with open(os.path.join(self.localpath, self.host, xml), "w", encoding="utf-8") as f:
                f.write(file_data)
            print("%s:中%s特殊字符替换完成!" % (self.host, xml))

    # 处理modbus_map.xml表
    def get_document_map(self):
        # todo 这里先设置mysql数据的全局变量 存储时候会报字符串太长的错误
        # self.__cur.execute('''set @@global.sql_mode='';''')
        # self.__conn.commit()
        """
        获取modbus_map.xml数据
        :return: map数据
        """
        # 替换特殊字符
        self.replace_str()
        with open(os.path.join(self.localpath, self.host, "modbus_map.xml"), 'r', encoding='utf-8') as f:
            # parse()获取DOM对象
            dom = minidom.parse(f)
            # print(dom)
            # 获取根节点
            root = dom.documentElement
            # 获取root根节点下所有子节点
            # child_list = root.childNodes
            signal_list = root.getElementsByTagName('signal')  # 是一个文档对象
            for signal in signal_list:
                dict_attr = {}  # 存储 数据 键值对的
                # 获取signal中所有属性名称得到一个列表  attributes.keys()
                for key in signal.attributes.keys():
                    key_add = signal.attributes[key]  # 这样得到的是一个地址
                    dict_attr[key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                self.modbus_map_list.append(dict_attr)  # 添加到列表
                # print(dict_attr)
            # print(self.modbus_map_list[0])
            # print(self.modbus_map_list[0][key])
            print("%s:modbus_map.xml表的数据有：%s条" % (self.host, len(self.modbus_map_list)))
            return self.modbus_map_list

    # 将MonitorUnitVTU.xml表存入数据库
    def get_document_vtu(self):
        """
        解析多个文档数据
        :return:
        """
        # 下载多个xml文件
        # self.download_files()
        # 获取中间xml文件数据(MonitorUnitVTU.xml)
        with open(os.path.join(self.localpath, self.host, "MonitorUnitVTU.xml"), 'r', encoding='utf-8') as f:
            # parse()获取DOM对象
            dom = minidom.parse(f)
            # print(dom)
            # 获取根节点
            root = dom.documentElement
            # 获取根节点下所有子节点的名称  根目录下节点对象：root.childNodes  遍历得到节点名称：i.nodeName
            for i in root.childNodes:
                # print(i.nodeName)
                # 得到一个子标签的文档对象
                tag_list = root.getElementsByTagName(i.nodeName)
                # print(tag_list)
                # 如果这个文档对象存在
                if tag_list:
                    for tag in tag_list:
                        # tag.childNodes得到Ports，Equipments，LogActions下的子标签对象
                        # print(tag.childNodes)
                        for child_tag in tag.childNodes:
                            # [‘CfgPort’,'CfgPort','CfgPort','#text','CfgEquipment','CfgEquipment',#text','EventLogAction','EventLogAction']
                            # 排除#text  遍历上述列表将得到的标签和==“CfgPort”作比对，满足条件
                            if child_tag.nodeName == "CfgPort":
                                port_dict = {}
                                # 获取子标签对象的属性名称: child_tag.attributes.keys()
                                for child_key in child_tag.attributes.keys():
                                    key_add = child_tag.attributes[child_key]
                                    port_dict[key_add.name] = key_add.value
                                # print(port_dict)
                                # 存入数据库
                                # 格式化当前时间
                                nowTime = datetime.datetime.now()
                                strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
                                data = [port_dict["PortId"], port_dict["PortNo"], port_dict["PortType"],
                                        port_dict["PortSetting"], port_dict["PortLibName"], port_dict["Description"],
                                        strTime, self.host]
                                # REPLACE存在就更新不存在就插入
                                sql_str = '''insert into tb_port (PortId, PortNo, PortType, PortSetting, PortLibName, Description, port_time, port_ip) values(%s, %s, %s, %s, %s, %s, %s, %s);'''
                                self.__cur.execute(sql_str, data)
                                self.__conn.commit()

                            elif child_tag.nodeName == "CfgEquipment":
                                # print(child_tag.nodeName)
                                quipment_dict = {}
                                # 获取子标签对象的属性名称: child_tag.attributes.keys()
                                for child_key in child_tag.attributes.keys():
                                    key_add = child_tag.attributes[child_key]
                                    quipment_dict[key_add.name] = key_add.value
                                # print(quipment_dict)
                                nowTime = datetime.datetime.now()
                                strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
                                data = [quipment_dict["EquipId"], quipment_dict["EquipTemplateId"],
                                        quipment_dict["EquipmentName"], quipment_dict["PortId"],
                                        quipment_dict["EquipAddress"], quipment_dict["LibName"], strTime, self.host]
                                sql_str = '''insert into tb_equipments (EquipId, EquipTemplateId, EquipmentName, PortId, EquipAddress, LibName, Equipment_time, Equipment_ip) values(%s, %s, %s, %s, %s, %s, %s, %s);'''
                                self.__cur.execute(sql_str, data)
                                self.__conn.commit()
                            elif child_tag.nodeName == "EventLogAction":
                                logaction_dict = {}
                                # 获取子标签对象的属性名称: child_tag.attributes.keys()
                                for child_key in child_tag.attributes.keys():
                                    key_add = child_tag.attributes[child_key]
                                    logaction_dict[key_add.name] = key_add.value
                                # 然后获取子标签的值
                                for i in child_tag.childNodes:
                                    if i.nodeName == 'Action':
                                        # print(i.nodeName)
                                        for key in i.attributes.keys():
                                            key_adds = i.attributes[key]
                                            # 因为子标签和上级标签有相同的属性名，为了避免覆盖掉，做判断。
                                            if key_adds.name != 'ActionName':
                                                logaction_dict[key_adds.name] = key_adds.value
                                            else:
                                                pass
                                # print('111111111111',logaction_dict)
                                nowTime = datetime.datetime.now()
                                strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
                                data = [logaction_dict["LogActionId"], logaction_dict["ActionName"],
                                        logaction_dict["TriggerType"], logaction_dict["ActionId"],
                                        logaction_dict["EquipmentId"], logaction_dict["ActionValue"], strTime,
                                        self.host]
                                sql_str = '''insert into tb_logactions (LogActionId, ActionName, TriggerType, ActionId, EquipmentId, ActionValue, logactions_time, logactions_ip) values(%s, %s, %s, %s, %s, %s, %s, %s);'''
                                self.__cur.execute(sql_str, data)
                                self.__conn.commit()
        print("-------------------------%s:Document_vtu 文件数据存入到数据库成功-------------------------" % self.host)

    # 批量存入EquipmentTemplate....表数据
    def get_documents(self):
        self.replaces_str()
        # 1.通过lsitdir获取xml名称列表
        catalog_list = os.listdir(os.path.join(self.localpath, self.host))
        # child_dict_list = []  # 这个列表存储所有的.xml文件信息
        for catalog in catalog_list:
            # 2.判断以EquipmentTemplate开头的.xml文件
            if catalog.startswith("EquipmentTemplate"):
                with open(os.path.join(self.localpath, self.host, catalog), 'r', encoding='utf-8') as f:
                    # print(catalog)
                    # parse()获取DOM对象
                    dom = minidom.parse(f)
                    # 获取dom的根节点
                    root = dom.documentElement
                    # 遍历dom根节点下还有一个根节点
                    # print(root.childNodes)
                    root_dict = {}  # 根节点的属性
                    child_dict = {}
                    # 1.获取根目录的属性值
                    for i in root.childNodes:
                        # print(i.nodeName)  # ['#text','<EquipTemplate>','#text']
                        # 判断当子目录有值时候（过滤）=>  获取根节点的属性
                        if i.childNodes:
                            # print(i.nodeName)
                            for key in i.attributes.keys():
                                key_add = i.attributes[key]  # 这样得到的是一个地址  得到根节点的属性
                                root_dict[key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                    # print(root_dict)  # 得到EquipTemplate节点内的所有属性
                    # print(root.childNodes.EquipTemplate)
                    for i in root.getElementsByTagName('EquipTemplate'):
                        for j in i.childNodes:
                            # print(j.nodeName)
                            """1、如果是Signals标签"""
                            if j.nodeName == 'Signals':
                                EquipSignal_list = j.childNodes
                                for EquipSignal in EquipSignal_list:
                                    # print(EquipSignal.nodeName)
                                    if EquipSignal.nodeName == "EquipSignal":
                                        # 1.获取每个子节点属性
                                        # 子节点的属性
                                        # print(EquipSignal.attributes.keys())
                                        for key in EquipSignal.attributes.keys():
                                            key_add = EquipSignal.attributes[key]  # 这样得到的是一个地址  得到根节点的属性
                                            child_dict[
                                                key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                                        child_dict.update(root_dict)  # 使用update合并 root目录的属性值   返回值是一个None
                                        """这里有个问题 如果是<Meanings />下面没有子节点的也要存储。
                                        """
                                        nowTime = datetime.datetime.now()
                                        # 格式化当前时间
                                        strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
                                        data = [child_dict.get("EquipTemplateId"),
                                                child_dict.get("EquipTemplateName"),
                                                child_dict.get("SignalId"),
                                                child_dict.get("SignalName"), child_dict.get("Unit"),
                                                self.host, strTime]
                                        sql_str = '''insert into tb_Signals_meaing (EquipTemplateId, EquipTemplateName, SignalId, SignalName, Unit, Signals_ip, Signals_time) values(%s, %s, %s, %s, %s, %s, %s);'''
                                        self.__cur.execute(sql_str, data)
                                        self.__conn.commit()
                                        # print(child_dict)
                                        # 2.获取子节点Meanings下一级的属性 告警的状态

                                        # if EquipSignal.nodeName == "SignalMeaning":
                                        for meation in EquipSignal.childNodes:
                                            # Meanings下一级的节点可能会不存在
                                            # print(meation.childNodes)
                                            if meation.childNodes:
                                                for sig_mean in meation.childNodes:
                                                    if sig_mean.nodeName != "#text":
                                                        Meanings_dict = {}
                                                        for key in sig_mean.attributes.keys():
                                                            key_add = sig_mean.attributes[key]  # 这样得到的是一个地址  得到根节点的属性
                                                            Meanings_dict[
                                                                key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                                                        # print(Meanings_dict)
                                                        child_dict.update(Meanings_dict)
                                                        # print(child_dict)
                                                        # 3.存入数据库
                                                        nowTime = datetime.datetime.now()
                                                        # 格式化当前时间
                                                        strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
                                                        # print('111111111111111111111111', child_dict)
                                                        data = [child_dict.get("EquipTemplateId"),
                                                                child_dict.get("EquipTemplateName"),
                                                                child_dict.get("SignalId"),
                                                                child_dict.get("SignalName"), child_dict.get("Unit"),
                                                                child_dict.get("StateValue"), child_dict.get("Meaning"),
                                                                self.host, strTime]
                                                        # print(data)
                                                        sql_str = '''insert into tb_Signals_meaing (EquipTemplateId, EquipTemplateName, SignalId, SignalName, Unit, StateValue, Meaning, Signals_ip, Signals_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);'''
                                                        self.__cur.execute(sql_str, data)
                                                        self.__conn.commit()
                            """2、如果是Events标签"""
                            if j.nodeName == 'Events':
                                Events_list = j.childNodes
                                for EquipSignal in Events_list:
                                    if EquipSignal.nodeName == "EquipEvent":
                                        # 1.获取每个子节点属性
                                        # 子节点的属性
                                        # print(EquipSignal.attributes.keys())
                                        for key in EquipSignal.attributes.keys():
                                            key_add = EquipSignal.attributes[key]  # 这样得到的是一个地址  得到根节点的属性
                                            child_dict[
                                                key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                                        child_dict.update(root_dict)  # 使用update合并 root目录的属性值   返回值是一个None
                                        """这里有个问题 如果是<EventCondition />下面没有子节点的也要存储。
                                                                                """
                                        nowTime = datetime.datetime.now()
                                        # 格式化当前时间
                                        strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
                                        data = [child_dict.get("EquipTemplateId"),
                                                child_dict.get("EquipTemplateName"),
                                                child_dict.get("EventId"),
                                                child_dict.get("EventName"),
                                                self.host, strTime]
                                        # print(data)
                                        sql_str = '''insert into tb_Events (EquipTemplateId, EquipTemplateName, EventId, EventName, Events_ip, Events_time) values(%s, %s, %s, %s, %s, %s);'''
                                        self.__cur.execute(sql_str, data)
                                        self.__conn.commit()

                                        # 2.获取子节点Meanings下一级的属性 告警的状态
                                        for meation in EquipSignal.childNodes:
                                            # Meanings下一级的节点可能会不存在
                                            # print(meation.childNodes)
                                            if meation.childNodes:
                                                for sig_mean in meation.childNodes:
                                                    if sig_mean.nodeName != "#text":
                                                        # print(sig_mean.nodeName)
                                                        Meanings_dict = {}
                                                        for key in sig_mean.attributes.keys():
                                                            key_add = sig_mean.attributes[key]  # 这样得到的是一个地址  得到根节点的属性
                                                            Meanings_dict[
                                                                key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                                                        # print(Meanings_dict)
                                                        child_dict.update(Meanings_dict)
                                                        # print(child_dict["EquipTemplateName"], child_dict["EventId"], child_dict["LibName"])
                                                        # 3.存入数据库
                                                        nowTime = datetime.datetime.now()
                                                        # 格式化当前时间
                                                        strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
                                                        # print('111111111111111111111111', child_dict)
                                                        data = [child_dict.get("EquipTemplateId"),
                                                                child_dict.get("EquipTemplateName"),
                                                                child_dict.get("EventId"),
                                                                child_dict.get("EventName"),
                                                                child_dict.get("ConditionId"),
                                                                child_dict.get("Meaning"),
                                                                child_dict.get("EventSeverity"),
                                                                child_dict.get("StartCompareValue"),
                                                                child_dict.get("StartOperation"),
                                                                self.host, strTime]
                                                        sql_str = '''insert into tb_Events (EquipTemplateId, EquipTemplateName, EventId, EventName, ConditionId, Meaning, EventSeverity,StartCompareValue,StartOperation,Events_ip, Events_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
                                                        self.__cur.execute(sql_str, data)
                                                        self.__conn.commit()
                            """3、如果是Commands标签"""
                            if j.nodeName == 'Commands':
                                pass
        print("-------------------------%sXml文件集数据存入到数据库成功-------------------------" % self.host)

    # 将数据实时存入
    def get_realtime_data(self):
        """
        通过modbus_tcp获取实时数据
        :return:
        """
        try:
            # 判断是否连接成功 （否 否为真）
            # is_open()取TCP连接状态    open()连接到Modbus服务器（开放的TCP连接）
            # print(self.__client.is_open())
            # print(self.__client.open())
            if not self.__client.is_open() and not self.__client.open():
                # 在次连接一次，没有连接上则抛出错误
                raise RuntimeError('无法连接：请检查%s端口或IP地址是否正确' % self.host)
            while True:
                # add_list = []
                if self.__address < len(self.modbus_map_list):

                    # time.sleep(3)
                    # if self.__address < len(self.modbus_map_list):
                    """
                    返回的源码：[FA 80 00 00 00 17 01] 03 14 00 00 3F 80 00 00 3F 80 00 00 3F 80 00 00 3F 80 66 66 41 E2 
                    自动解析的数据：[0, 16256, 0, 16256, 0]
                    1.改写方法(read_holding_registers)：源码返回的数据为 00 00 3F 80位 只解析00 00位和3F 80位，通过调试模式返Rx数据，返回数据为（registers, re_debug）
                    2.开启调试模式获re_debug
                    3.
                    """
                    # registers, re_debug = self.__client.read_holding_registers(self.__address, self.__register)
                    registers, debug_data = self.__client.read_holding_registers(self.__address, self.__register)
                    # 获取50个数据（字符串类型）
                    # print(utils.word_list_to_long(debug_data))
                    str_list = debug_data.split(" ")[9:-1]
                    # print(str_list)
                    a = [str_list[x:x + 4] for x in range(0, len(str_list), 4)]
                    # 这里打印接收的数量条数。
                    for x in a:
                        # 将每一个数据合并成一个字符串
                        b = "".join(x)
                        # print(b)
                        # 调整字符串的位置前面四位不动 后面四位两两交换位置（注意转浮点数时候大端小端问题）
                        c = b[0:4] + b[-2:] + b[4:6]
                        # print(c)
                        # 4位16进制数 转浮点数
                        d = "%.2f" % struct.unpack('<f', bytes.fromhex(c))[0]
                        # print("%d正在获取(%s)的数据: %s" % (self.i, self.modbus_map_list[self.i], d))
                        print("%s的第%s数据为%s" % (self.host, self.i, d))

                        # add_list.append(d)
                        print(d)
                        print(str(d))
                        # 存入数据库
                        self.input_data(d)
                        self.i += 1
                    # self.__address += 50
                    self.__address += 1
                    # print(add_list)
                else:
                    self.i = 0
                    self.__address = 0
                    time.sleep(0.5)
                    break
        except:
            pass

    # 6.map表存入数据库
    def input_data(self, float_data):
        # 将得到的浮点数数据存入到数据库
        # 获取当前时间
        nowTime = datetime.datetime.now()
        # 格式化当前时间
        strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
        # print(strTime)
        # 逻辑删除（在drf中自定义模型，逻辑删除健，设置了默认值，但是只有通过drf存储时才会有默认值，直接在数据库中存储是不会添加默认值的）
        # is_delete = False
        # divice_ip = self.iptoint(self.host)
        # divice_ip = self.host
        # print(type(divice_ip))
        data = [self.modbus_map_list[self.i]["equipid"], self.modbus_map_list[self.i]["sigid"],
                self.modbus_map_list[self.i]["reg_addr"],
                self.modbus_map_list[self.i]["name"], float_data, strTime, False, self.host]
        sql_str = '''insert into tb_xmldata (equipid, sigid, reg_addr, name, float_data, data_time, is_delete, divice_ip) values(%s, %s, %s, %s, %s, %s, %s, %s);'''
        self.__cur.execute(sql_str, data)
        self.__conn.commit()


if __name__ == "__main__":
    # ftp = Ftp_Data("192.168.1.30")
    # ftp.get_document_map()
    # ftp.get_document_vtu()
    # ftp.get_documents()
    def run(ip):
        ftp = Ftp_Data(ip)
        ftp.get_document_map()  # 1.获取map表 需要先运行这个函数
        ftp.get_document_vtu()  # 将MonitorUnitVTU.xml数据存入mysql数据库 一次性
        ftp.get_documents()  # 批量存入EquipmentTemplate....表数据
        while True:
            ftp.get_realtime_data()  # 2.获取事实数据
    # 配置线程
    ip_list = []  # ip池要是元组("192.168.1.20",), ("192.168.1.30",), ("192.168.1.40",)
    threads = []  # 线程池
    def con_mysql():
        ip_list.clear()
        # 1.查询数据库设备表所有信息 得到ip池
        conn = connect(host='localhost', port=3306, database="MOTTA_data", user="root", password="mysql", charset="utf8")
        cur = conn.cursor()
        sql_str = ''' select * from tb_divices;'''
        cur.execute(sql_str)
        # 遍历输出所有的结果 t是元组
        for t in cur.fetchall():
            ip_list.append((t[1],))  # 添加元组到列表
    # 调用查询数据库函数，得到ip_list
    con_mysql()

    # 如果ip_list列表为[]，则5分钟循环一次.跳出循环条件为ip列表有数据。
    if len(ip_list) == 0:
        # 如果ip池没有数据
        while True:
            time.sleep(300)
            # 等待5分钟后再次连接数据
            con_mysql()
            # 如果ip池有数据了就跳出循环
            print("数据库没有ip站点")
            if len(ip_list) != 0:
                print("数据库有ip站点，跳出循环，执行下一步")
                break

    # 2.添加线程到线程池
    for i in range(len(ip_list)):
        t = threading.Thread(target=run, args=ip_list[i])
        threads.append((t, i))
    print("从tb_port表获取ip列表：%s" % ip_list)
    print("打印生成的线程列表：%s" % threads)
    for i in threads:
        i[0].start()
        print("开启线程：%s" % i[0])
    while True:
        # 将ip_list的值赋值给flag_list
        flag_list = copy.copy(ip_list)
        # 获取新的ip_list
        con_mysql()
        # 如果flag_list == ip_list
        if flag_list == ip_list:
            for i in threads:
                if i[0].is_alive() is False:
                    print("%s线程的状态为：%s" % (i[0], i[0].is_alive()))
                    threads.remove(i)
                    t = threading.Thread(target=run, args=ip_list[i[1]])
                    threads.append(t)  # 将挂掉的线程添加 到线程池
                    t.start() # 开启
        else:
            # 获取的新的ip列表不相等。1、先移除旧的线程。2、添加开启新的线程
            print("检测到站点发生了变化......")
            for i in threads:
                threads.remove(i)
                print(threads)
            for i in range(len(ip_list)):
                t = threading.Thread(target=run, args=ip_list[i])
                threads.append((t, i))
            for i in threads:
                i[0].start()
                print("开启线程：%s" % i[0])
        time.sleep(60)  # 20秒检测一次
        print("间隔60秒，检测线程池的状态....")