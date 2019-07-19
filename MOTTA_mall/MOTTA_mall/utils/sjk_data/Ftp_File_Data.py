# coding: utf-8
from ftplib import FTP
import os

class Ftp_Data(object):
    def __init__(self):
        # self.host = input("请输入IP地址：")
        # self.port = int(input("请输入端口号："))
        # self.username = input("请输入用户名：")
        # self.password = input("请输入密码：")
        self.host = "192.168.1.200"
        self.port = 2121
        self.username = "ftp"
        self.password = "ftp"
        self.remotepath = "/data/mgrid/sampler/modbus_map.xml"
        self.sopath = "/data/mgrid/sampler/SO"
        self.xmlpath = "/data/mgrid/sampler/XmlCfg"
        self.vtupath = "/sdcard/vtu_pagelist"
        self.deletepath = "/sdcard/tmp/reboot.txt"   #重启

    def ftp_connect(self):
        ftp = FTP()
        # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
        ftp.connect(self.host, self.port)  # 连接
        ftp.login(self.username, self.password)  # 登录，如果匿名登录则用空串代替即可
        return ftp

    def download_file(self):
        ftp = self.ftp_connect()
        # 下载文件
        bufsize = 1024  # 设置缓冲块大小
        fp = open("./modbus_map.xml", 'wb')  # 以写模式在本地打开文件
        ftp.retrbinary('RETR ' + self.remotepath, fp.write, bufsize)  # 接收服务器上文件并写入本地文件
        ftp.set_debuglevel(0)  # 关闭调试
        fp.close()  # 关闭文件
        self.ftp_connect().quit()

    def upload_file(self):
        # 上传文件
        ftp = self.ftp_connect()
        ftp.rmd(self.sopath)  # 删除远程目录
        bufsize = 1024
        # fp = open("./modbus_map.xml", 'rb')
        # ftp.storbinary('STOR ' + self.remotepath, fp, bufsize)  # 上传文件
        # ftp.set_debuglevel(0)
        # fp.close()
        self.ftp_connect().quit()

    def delete_file(self):
        # 删除重启文件 重启机器
        ftp = self.ftp_connect()
        ftp.delete(self.deletepath)
        self.ftp_connect().quit()


if __name__ == "__main__":
    ftp = Ftp_Data()
    ftp.download_file()
    # ftp.upload_file()
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
ftp.storbinaly("STOR filename.txt",file_handel,bufsize)#上传目标文件
ftp.retrbinary("RETR filename.txt",file_handel,bufsize)#下载FTP
"""