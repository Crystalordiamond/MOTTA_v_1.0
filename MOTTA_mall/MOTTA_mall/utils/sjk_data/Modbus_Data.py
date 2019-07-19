import time
from pyModbusTCP.client import ModbusClient
import struct


class Float_Data(object):
    def __init__(self):
        self.__client = ModbusClient(host="192.168.1.200", port=502, auto_open=True)
        self.__address = 0
        self.__register = 2
        self.__hex_str_list = []
        self.__hex_data = []
        self.float_list = []
        # self.float_data = ""

    def Get_Data(self):
        if not self.__client.is_open():
            if not self.__client.open():
                raise RuntimeError('无法连接：请检查端口或IP地址是否正确')
        while True:
            if self.__client.is_open():
                regs = self.__client.read_holding_registers(self.__address, self.__register)
                # regs = self.__client.read_discrete_inputs(self.__address, self.__register)
                # if success display registers
                if regs:
                    # print(regs)
                    # "".join()是将列表里面的字符串拼接  '{:x}'.format() 将十进制转换成十六进制 04目前理解为前面补0 将十进制转换成十六进制字符串
                    Hex_str = "".join('{:04x}'.format(x) for x in regs)

                    # 1个寄存器4个字节，其中，低16位先发，高16位后发，每16位高8位在前，低8位在后
                    for i in Hex_str:

                        self.__hex_str_list.append(i)
                    if self.__hex_str_list[2]:
                        self.__hex_data.append(self.__hex_str_list[2])
                    if self.__hex_str_list[3]:
                        self.__hex_data.append(self.__hex_str_list[3])
                    if self.__hex_str_list[0]:
                        self.__hex_data.append(self.__hex_str_list[0])
                    if self.__hex_str_list[1]:
                        self.__hex_data.append(self.__hex_str_list[1])
                    if self.__hex_str_list[6]:
                        self.__hex_data.append(self.__hex_str_list[6])
                    if self.__hex_str_list[7]:
                        self.__hex_data.append(self.__hex_str_list[7])
                    if self.__hex_str_list[4]:
                        self.__hex_data.append(self.__hex_str_list[4])
                    if self.__hex_str_list[5]:
                        self.__hex_data.append(self.__hex_str_list[5])
                    # 将位置调换后的字符串

                    a = "".join(self.__hex_data)
                    # 将十六进制转化为浮点数 小端
                    float_data = "%.2f" % struct.unpack('<f', bytes.fromhex(a))[0]
                    # print("寄存器：%d 的值为:%s 转化成浮点数后：%s" % (self.__address, str(regs), float_data))
                    self.float_list.append(float_data)
                    self.__hex_str_list.clear()
                    self.__hex_data.clear()
                    # print(self.float_list)

                    # print("正在更新数据%s,请稍候......" % (self.__address))
                    self.__address += 1
                    # if self.__address == 10:
                    #     break

                else:
                    print("数据获取完成......")
                    # 他们自定义的协议，每2za个寄存器获得一个浮点数，最后一位时候只能获取一个寄存器，无法显示浮点数，所以添加一个状态码。
                    self.float_list.append(1)
                    break

    def back_data(self):
        self.Get_Data()
        return self.float_list

    def __delete__(self):
        self.float_list.clear()
        print(self.float_list)

if __name__ == '__main__':
    float_data = Float_Data()
    float_data.back_data()
    # float_data.__delete__()
