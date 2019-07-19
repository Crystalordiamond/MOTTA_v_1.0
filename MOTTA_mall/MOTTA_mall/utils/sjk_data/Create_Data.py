import time
import datetime
from pymysql import connect
from MOTTA_mall.MOTTA_mall.utils.sjk_data.Ftp_File_Data import Ftp_Data
from MOTTA_mall.MOTTA_mall.utils.sjk_data.Modbus_Data import Float_Data
from MOTTA_mall.MOTTA_mall.utils.sjk_data.Get_File_Data import Xml_Data


class CreateData(object):
    def __init__(self):
        self.__conn = connect(host='localhost', port=3306, database="MOTTA_data", user="root", password="mysql",
                              charset="utf8")
        self.__cur = self.__conn.cursor()
        # 初始化数据获取 这样初始化只是得到了一个列表 做法是错误的
        # self.float_data = Float_Data().back_data()

        # 初始化map表， 只需要使用一次，循环时候会浪费时间
        self.type_data = self.map_list()

    def map_list(self):
        # 通过ftp远程获取文件
        Ftp_Data().download_file()
        # 获取xml文件中的字段([...],[...],[...],[...])tuple元组类型
        type_data = Xml_Data().get_file()
        return type_data

    def __add__(self):
        start = time.time()
        # 获取浮点数数据 [...,...,...,...,...] 在循环里面调用方法再赋值
        float_data = Float_Data().back_data()
        print(float_data)
        end = time.time()
        print("获取寄存器数据时间：%s秒" % (end - start))
        start1 = time.time()
        # 分别获得equipid sigid red_addr name 的数据列表
        equipid, sigid, reg_addr, name = self.type_data[0], self.type_data[1], self.type_data[2], self.type_data[3]
        print(len(name))
        print(len(float_data))
        for i in range(len(float_data)):
            nowTime = datetime.datetime.now()
            strTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
            divice_delete = 1
            data = [equipid[i], sigid[i], reg_addr[i], name[i], float_data[i], strTime, divice_delete]
            sql_str = '''insert into tb_xmldata (equipid, sigid, reg_addr, name, float_data, data_time, divice_id_id) values(%s, %s, %s, %s, %s, %s, %s);'''
            self.__cur.execute(sql_str, data)
            self.__conn.commit()

        float_data.clear()
        end1 = time.time()
        print("存储条数据到数据库时间为：%s秒" % (end1 - start1))

    def fetch_all_info(self):
        # 查询所有信息s
        sql_str = ''' select * from monitor_Center_1;'''
        self.__cur.execute(sql_str)
        # 遍历输出所有的结果
        for t in self.__cur.fetchall():
            print(t)

    def delete_data(self):
        # 删除所有表
        sql_str = '''select concat('delete from ',table_name,';') from information_schema.TABLES where table_schema='MOTTA_data';'''
        self.__cur.execute(sql_str)
        for t in self.__cur.fetchall():
            sql_tuple = '''%s''' % t[0]
            self.__cur.execute(sql_tuple)
        self.__conn.commit()
        print("清除所有表数据成功！！！")

    def updata_data(self):
        sql_str = '''updata monitor_Center_1 set display_order=float_data where id=1'''

    def __del__(self):
        # 将数据库关闭操作放到 __del__方法中，当对象销毁时，自动关闭数据库
        self.__cur.close()
        self.__conn.close()


if __name__ == '__main__':
    data = CreateData()
    # data.create()  # 创建表
    # data.__add__()
    while True:
        data.__add__()
