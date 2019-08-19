from ftplib import FTP
import xml.dom.minidom as xmldom
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import struct
from pymysql import connect
import datetime
import time
from multiprocessing import Queue
import threading


class Storage_Data(object):
    def __init__(self):
        # self.host = input("请输入IP地址：")
        # self.port = int(input("请输入端口号："))
        # self.username = input("请输入用户名：")
        # self.password = input("请输入密码：")
        self.host = "192.168.1.200"
        self.port = 2121
        self.username = "ftp"
        self.password = "ftp"
        self.remote_path = "/data/mgrid/sampler/modbus_map.xml"
        self.__file = "./modbus_map.xml"
        self.__old_str = "&"
        self.__new_str = "-"
        self.equipid_list = []
        self.sigid_list = []
        self.reg_addr_list = []
        self.name_list = []
        self.__client = ModbusClient(host=self.host, port=502, debug=True, auto_open=True)
        self.__address = 0
        self.__register = 50
        self.i = 0
        self.__conn = connect(host='localhost', port=3306, database="MOTTA_data", user="root", password="mysql",
                              charset="utf8")
        self.__cur = self.__conn.cursor()
        self.float_data = []  # 检测获取到的数据

    # 1.获取map表（xml格式）
    def ftp_connect(self):
        # 初始化FTP
        ftp = FTP()
        # 连接IP地址和端口
        ftp.connect(self.host, self.port)
        # 输入帐号密码登录，如果匿名登录则用空串代替即可
        ftp.login(self.username, self.password)
        # 返回FTP对象
        return ftp

    # 2.下载xml文件
    def download_file(self):
        # 调用ftp_connect()方法 下载文件
        ftp = self.ftp_connect()
        # 设置缓冲块大小
        bufsize = 1024
        # 以写模式在本地打开文件(当前目录)
        fp = open("./modbus_map.xml", 'wb')
        # 接收服务器上文件并写入本地文件
        ftp.retrbinary('RETR ' + self.remote_path, fp.write, bufsize)
        # 关闭文件
        fp.close()
        # 退出FTP
        self.ftp_connect().quit()

    # -------------------------------------《处理下载的xml文件》--------------------------------------------------

    # 3.替换字符串&，符串&在xml文件中属于特殊字符串，在解析获取xml文件内容时会因为字符串报错
    def replace_string(self):
        self.download_file()
        # 将xml文件中的&替换成-(XML文件有五个不允许出现的特殊字符)
        file_data = ""
        # 打开下载到本地的xml文件
        with open(self.__file, "r", encoding="utf-8") as f:
            # 遍历xml文件行
            for line in f:
                if self.__old_str in line:
                    # Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
                    line = line.replace(self.__old_str, self.__new_str)
                file_data += line
        # w：打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
        with open(self.__file, "w", encoding="utf-8") as f:
            # 替换含有$字符串的行
            f.write(file_data)

    # 4.获取数据列表(equipid=[...] sigid=[...] reg_addr=[...] name=[...])
    def get_data_list(self):
        self.replace_string()
        # 打开下载到本地的xml文档对象
        dom = xmldom.parse(self.__file)
        # 得到文档元素对象 documentElement 属性可返回文档的根节点。
        root = dom.documentElement
        # getElementsByTagName() 方法可返回带有指定标签名的对象的集合（是一个文档对象）
        document_object = root.getElementsByTagName('signal')
        # 遍历<signal>标签 对象集合
        for item in document_object:
            # getAttribute()方法返回指定属性名的属性值。
            equipid = item.getAttribute("equipid")
            # 将获取的‘equipid’属性值，存到equipid_list列表中
            self.equipid_list.append(equipid)
            sigid = item.getAttribute("sigid")
            self.sigid_list.append(sigid)
            reg_addr = item.getAttribute("reg_addr")
            self.reg_addr_list.append(reg_addr)
            name = item.getAttribute("name")
            self.name_list.append(name)

    # -------------------------------------《IP地址和int类型的互相转换》---------------------------------------
    # IP转int型
    def iptoint(self, num):
        list = []
        s = num.split(".")
        for temp in s:
            a = bin(int(temp))[2:]
            a = a.zfill(8)
            list.append(a)
        g = "".join(list)
        e = int(g, 2)
        return e

    def inttoip(self, num):
        s = bin(num)[2:]
        s = s.zfill(32)
        g = []
        h = []
        for i in range(0, 32, 8):
            g.append(s[i:i + 8])
        for temp in g:
            h.append(str(int(temp, 2)))
        e = ".".join(h)
        return e

    # -------------------------------------《通过modbus-tcp协议获取实时数据》---------------------------------------

    # 5.实时更新数据并添加到数据库(实时通过while循环反复存储)
    def get_realtime_data(self):
        # 判断是否连接成功 （否 否为真）
        if not self.__client.is_open() and not self.__client.open():
            # 在次连接一次，没有连接上则抛出错误
            raise RuntimeError('无法连接：请检查端口或IP地址是否正确')
        while True:
            # time.sleep(3)
            if self.__address < len(self.name_list):
                """
                1.改写源码(read_holding_registers)：源码返回的数据为32位 协议为64位数据对不上，通过调试模式返Rx数据，返回数据为（registers, re_debug）
                2.开启调试模式获re_debug 
                """
                registers, re_debug = self.__client.read_holding_registers(self.__address, self.__register)
                # 获取50个数据（字符串类型）
                # print(re_debug)
                str_list = re_debug.split(" ")[9:-1]
                a = [str_list[x:x + 4] for x in range(0, len(str_list), 4)]
                # print(len(a))
                for x in a:
                    b = "".join(x)
                    # print(b)
                    # 前面四位不动 后面四位两两交换位置（注意转浮点数时候大端小端问题）
                    c = b[0:4] + b[-2:] + b[4:6]
                    # print(c)
                    # 4位16进制数 转浮点数
                    d = "%.2f" % struct.unpack('<f', bytes.fromhex(c))[0]
                    # print("%d正在获取(%s)的数据: %s" % (self.i, self.name_list[self.i], d))
                    self.input_data(d)
                    self.i += 1
                self.__address += 50
            else:
                self.i = 0
                self.__address = 0
                # time.sleep(3)
                break

    # 6.存入数据库
    def input_data(self, float_data):

        # 将得到的浮点数数据存入到数据库
        # 获取当前时间
        nowTime = datetime.datetime.now()
        # 格式化当前时间
        strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
        # 逻辑删除（在drf中自定义模型，逻辑删除健，设置了默认值，但是只有通过drf存储时才会有默认值，直接在数据库中存储是不会添加默认值的）
        is_delete = False
        # divice_ip = self.iptoint(self.host)
        divice_ip = self.host
        # print(type(divice_ip))
        data = [self.equipid_list[self.i], self.sigid_list[self.i], self.reg_addr_list[self.i],
                self.name_list[self.i], float_data,
                strTime, is_delete, divice_ip]
        sql_str = '''insert into tb_xmldata (equipid, sigid, reg_addr, name, float_data, data_time, is_delete, divice_ip) values(%s, %s, %s, %s, %s, %s, %s, %s);'''
        self.__cur.execute(sql_str, data)
        self.__conn.commit()


if __name__ == "__main__":
    ftp = Storage_Data()
    ftp.get_data_list()
    while True:
        # start = time.time()
        ftp.get_realtime_data()
        # end = time.time()
        print(datetime.datetime.now())

