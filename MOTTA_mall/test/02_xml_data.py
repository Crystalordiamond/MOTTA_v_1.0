from ftplib import FTP
from xml.dom import minidom
from pyModbusTCP.client import ModbusClient
import struct
import os, time


class Ftp_Data(object):
    """
    用来获取xml文件和替换需要更改的文件
    """

    def __init__(self):
        self.host = "192.168.1.30"
        self.port = 2121
        self.username = "ftp"
        self.password = "ftp"
        self.localpath = "./"
        self.modbus_xml = "/data/mgrid/sampler/modbus_map.xml"
        self.XmlCfg_ftp_path = "/data/mgrid/sampler/XmlCfg"
        self.vtu_pagelist_ftp_path = "/sdcard/vtu_pagelist/"

        self.__old_str = "&"
        self.__new_str = "-"

        # self.__client = ModbusClient(host=self.host, port=502)
        self.__client = ModbusClient(host=self.host, port=502, debug=True, auto_open=True)
        self.modbus_map_list = []  # 存储modbus_map_list表数据[{},{},{}...]
        self.MonitorUnitVTU = []  # 存储MonitorUnitVTU表数据[{},{},{}...]

        self.name_list = []
        self.__address = 0
        self.__register = 50
        self.i = 0

    def ftp_connect(self):
        """ 连接ftp """
        # 实例化FTP对象
        self.ftp = FTP()
        # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
        try:
            self.ftp.connect(self.host, self.port)  # 连接
        except:
            raise IOError("ftp connect failed!")
        try:
            self.ftp.login(self.username, self.password)  # 登录，如果匿名登录则用空串代替即可
        except:
            raise IOError("ftp login failed!")
        else:
            print("FTP connection successful......")

    def download_file(self):
        # 连接ftp()
        self.ftp_connect()
        """
        下载modbus_map.xml文件
        """
        # exists()判断当前路径 是否有self.host文件夹
        if os.path.exists(os.path.join(self.localpath, self.host)):
            pass
        else:
            # 创建当前文件夹
            os.mkdir(os.path.join(self.localpath, self.host))
        # 下载文件
        bufsize = 1024  # 设置缓冲块大小
        # 以写模式在本地打开文件
        fp = open(os.path.join(self.localpath, self.host, "modbus_map.xml"), 'wb')
        # 接收服务器上文件并写入本地打开的文件
        self.ftp.retrbinary('RETR ' + self.modbus_xml, fp.write, bufsize)
        # ftp.set_debuglevel(0)  # 关闭调试
        fp.close()  # 关闭文件
        print("-------------------------Modbus_map.xml download completes-------------------------")
        # 关闭连接

    def download_files(self):
        # 连接ftp()
        self.ftp_connect()
        # exists()判断当前路径 是否有self.host文件夹
        if os.path.exists(os.path.join(self.localpath, self.host)):
            pass
        else:
            # 创建当前文件夹
            os.mkdir(os.path.join(self.localpath, self.host))
        """批量下载XmlCfg中xml文件"""
        file_list = self.ftp.nlst(self.XmlCfg_ftp_path)  # 获取下载的文件目录
        # print(file_list)
        files_list = []
        # 过滤非.xml文件结尾的文件
        for i in file_list:
            # 匹配以.xml结尾的文件名称
            if i.endswith('.xml') == True:
                files_list.append(i)
        bufsize = 1024 * 1024
        print("-------------------------Start the download-------------------------")
        # print(files_list)
        for i in files_list:
            # 以写模式在本地打开文件
            fp = open(os.path.join(self.localpath, self.host, i), 'wb')
            # 接收服务器上文件并写入本地打开的文件
            self.ftp.retrbinary('RETR ' + self.XmlCfg_ftp_path + '/' + i, fp.write, bufsize)
            # ftp.set_debuglevel(0)  # 关闭调试
            fp.close()  # 关闭文件
            print("文件%s下载完成" % i)
        print("-------------------------File download completes-------------------------")

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
        print("modbus_map.xml中特殊字符替换完成!")

    def get_document(self):
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
            # # 打印根节点名称 <conf>
            # print("打印根节点名称:%s" % root.nodeName)
            # # 打印根节点类型
            # print("打印根节点类型:%s" % root.nodeType)
            # # 打印根节点属性
            # print("打印根节点属性:%s" % root.nodeValue)

            # 获取root根节点下所有子节点
            # child_list = root.childNodes
            signal_list = root.getElementsByTagName('signal')  # 是一个文档对象 todo 最好是能自动获取到这个标签名称
            for signal in signal_list:
                dict_attr = {}  # 存储 数据 键值对的
                # 获取signal中所有属性名称得到一个列表  attributes.keys()
                for key in signal.attributes.keys():
                    key_add = signal.attributes[key]  # 这样得到的是一个地址
                    dict_attr[key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                self.modbus_map_list.append(dict_attr)  # 添加到列表
                # print(dict_attr)
            print("modbus_map.xml表的数据有：%s条" % len(self.modbus_map_list))
            return self.modbus_map_list

    def get_documents(self):
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
                tag_list = root.getElementsByTagName(i.nodeName)
                if tag_list:
                    for tag in tag_list:
                        print(tag.nodeName)

            # print(root.attributes.keys())
            signal_list = root.getElementsByTagName('signal')  # 是一个文档对象 todo 最好是能自动获取到这个标签名称
            for signal in signal_list:
                dict_attr = {}  # 存储 数据 键值对的
                # 获取signal中所有属性名称得到一个列表  attributes.keys()
                for key in signal.attributes.keys():
                    key_add = signal.attributes[key]  # 这样得到的是一个地址
                    dict_attr[key_add.name] = key_add.value  # key_add.name为属性名称 key_add.value为属性值
                self.modbus_map_list.append(dict_attr)  # 添加到列表
                # print(dict_attr)
            # print("modbus_map.xml表的数据有：%s条" % len(self.modbus_map_list))
            return self.modbus_map_list
        # 5.实时更新数据并添加到数据库(实时通过while循环反复存储)

    def get_realtime_data(self):
        """
        通过modbus_tcp获取实时数据
        :return:
        """
        # 判断是否连接成功 （否 否为真）
        # is_open()取TCP连接状态    open()连接到Modbus服务器（开放的TCP连接）
        # print(self.__client.is_open())
        # print(self.__client.open())
        if not self.__client.is_open() and not self.__client.open():
            # 在次连接一次，没有连接上则抛出错误
            raise RuntimeError('无法连接：请检查端口或IP地址是否正确')
        while True:
            # time.sleep(3)
            # if self.__address < len(self.name_list):
            """
            返回的源码：[FA 80 00 00 00 17 01] 03 14 00 00 3F 80 00 00 3F 80 00 00 3F 80 00 00 3F 80 66 66 41 E2 
            自动解析的数据：[0, 16256, 0, 16256, 0]
            1.改写方法(read_holding_registers)：源码返回的数据为 00 00 3F 80位 只解析00 00位和3F 80位，通过调试模式返Rx数据，返回数据为（registers, re_debug）
            2.开启调试模式获re_debug 
            """
            # registers, re_debug = self.__client.read_holding_registers(self.__address, self.__register)
            registers, debug_data = self.__client.read_holding_registers(self.__address, self.__register)
            # 获取50个数据（字符串类型）
            # print(debug_data)
            # print(registers)
            str_list = debug_data.split(" ")[9:-1]
            # print(str_list)
            a = [str_list[x:x + 4] for x in range(0, len(str_list), 4)]
            # 这里打印接收的数量条数。
            print(len(a))
            for x in a:
                # 将每一个数据合并成一个字符串
                b = "".join(x)
                # print(b)
                # 调整字符串的位置前面四位不动 后面四位两两交换位置（注意转浮点数时候大端小端问题）
                c = b[0:4] + b[-2:] + b[4:6]
                # print(c)
                # 4位16进制数 转浮点数
                d = "%.2f" % struct.unpack('<f', bytes.fromhex(c))[0]
                # print("%d正在获取(%s)的数据: %s" % (self.i, self.name_list[self.i], d))
                print(d)
                self.i += 1
            self.__address += 50


if __name__ == "__main__":
    ftp = Ftp_Data()
    # ftp.get_document()  # 获取modbus_map.xml数据
    ftp.get_documents()  # 批量下载xml文件
    # ftp.get_realtime_data()  # 事实获取数据

    # ftp.download_files()  # 批量下载xml文件
    # ftp.delete_file() # 重启机器
"""
ftp.cwd(pathname)#设置FTP当前操作的路径
ftp.dir()#显示目录下文件信息
ftp.nlst()#获取目录下的文件
ftp.mkd(pathname)#新建远程目录
ftp.pwd()#返回当前所在位置
ftp.rmd(dirname)#删除远程目录
ftp.delete(filename)#删除远程文件
ftp.rename(fromname, toname)#将fromname修改名称为toname。
ftp.storbinaly("STOR filename.txt",file_handel,bufsize)#上传目标文件e
ftp.retrbinary("RETR filename.txt",file_handel,bufsize)#下载FTP
"""
