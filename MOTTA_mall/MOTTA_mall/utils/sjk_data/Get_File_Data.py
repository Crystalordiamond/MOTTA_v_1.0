# coding=utf-8
import xml.dom.minidom as xmldom

'''获取从机上map表对应的数据字段，然后存入数据库'''

class Xml_Data(object):
    def __init__(self):
        # self.__file = "/home/python/Desktop/modbus_map.xml"
        self.__file = "./modbus_map.xml"
        self.__old_str = "&"
        self.__new_str = "-"
        self.equipid_list = []
        self.sigid_list = []
        self.reg_addr_list = []
        self.name_list = []

    def replace_file(self):
        # 将xml文件中的&替换成-    XML文件有五个不允许出现的特殊字符
        file_data = ""
        with open(self.__file, "r", encoding="utf-8") as f:
            # 遍历的每一行
            for line in f:
                if self.__old_str in line:
                    # Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
                    line = line.replace(self.__old_str, self.__new_str)
                file_data += line
        with open(self.__file, "w", encoding="utf-8") as f:
            f.write(file_data)

    def get_file(self):
        self.replace_file()
        dom = xmldom.parse(self.__file)
        # 得到文档元素对象
        root = dom.documentElement
        itemlist = root.getElementsByTagName('signal')  # 是一个文档对象

        for item in itemlist:
            equipid = item.getAttribute("equipid")
            self.equipid_list.append(equipid)
            sigid = item.getAttribute("sigid")
            self.sigid_list.append(sigid)
            reg_addr = item.getAttribute("reg_addr")
            self.reg_addr_list.append(reg_addr)
            name = item.getAttribute("name")
            self.name_list.append(name)
        print("map表数据数量：%s条" % len(self.name_list))
        return self.equipid_list, self.sigid_list, self.reg_addr_list, self.name_list


if __name__ == '__main__':
    file = Xml_Data()
    file.get_file()
