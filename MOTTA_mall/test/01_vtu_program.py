import sys
from ftplib import FTP
import os, time

_XFER_FILE = 'FILE'  # 传送文件
_XFER_DIR = 'DIR'  # 传送目录


class Ftp_Data(object):
    """
    用来烧录程序
    """

    def __init__(self):
        self.ftp = None

        # self.host = input("请输入ip地址")
        self.host = "192.168.1.30"
        self.port = 2121
        self.username = "ftp"
        self.password = "ftp"
        self.SO_path = "./vtu_config/sampler/SO/"
        self.SO_ftp_path = "/data/mgrid/sampler/SO/"

        self.XmlCfg_path = "./vtu_config/sampler/XmlCfg/"
        self.XmlCfg_ftp_path = "/data/mgrid/sampler/XmlCfg/"

        self.vtu_pagelist_path = "./vtu_config/vtu_pagelist"
        self.vtu_pagelist_ftp_path = "/sdcard/vtu_pagelist/"

        self.reboot_path = "/sdcard/tmp/reboot.txt"  # 重启

    def ftp_connect(self):
        if self.ftp is None:
            """ 连接ftp """
            # 实例化FTP对象
            self.ftp = FTP()
            self.ftp.encoding = "utf-8"
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
                print("FTP connection successful/FTP 连接成功")

    def upload_SO_files(self):
        """上传so文件数据"""
        try:
            self.ftp_connect()
            # 1.获取so文件夹内的文件列表,通过os.listdir函数
            file_path = os.listdir(self.SO_path)
            bufsize = 1024
            for i in file_path:
                fp = open(self.SO_path + i, 'rb')
                self.ftp.storbinary('STOR ' + self.SO_ftp_path + i, fp, bufsize)  # 上传文件
                # # ftp.set_debuglevel(0)
                fp.close()
                print("%s文件上传完成" % i)
            print("------------------SO文件上传完成------------------")
        except:
            raise IOError("SO文件上传出错...")

    def upload_XmlCfg_files(self):
        """上传XmlCfg文件数据"""
        try:
            self.ftp_connect()
            # 1.获取so文件夹内的文件列表,通过os.listdir函数
            file_path = os.listdir(self.XmlCfg_path)
            bufsize = 1024
            for i in file_path:
                fp = open(self.XmlCfg_path + i, 'rb')
                self.ftp.storbinary('STOR ' + self.XmlCfg_ftp_path + i, fp, bufsize)  # 上传文件
                # # ftp.set_debuglevel(0)
                fp.close()
                print("%s文件上传完成" % i)
            print("------------------XmlCfg文件上传完成------------------")
        except:
            raise IOError("XmlCfg文件上传出错...")

    def upload_vtu_pagelist_files(self):
        """上传vtu_pagelist文件夹数据  上传文件夹需要用到递归"""
        # 调用self.ftp_connect()生成全局的self.ftp对象
        self.ftp_connect()
        # 1.调用__filetype(self, src)方法 判断传入的”路径字符串“是文件夹还是文件（src）
        filetype, filename = self.__filetype()
        print("src类型是：%s" % filetype)
        # 如果是目录
        if filetype == _XFER_DIR:
            # 调用upload_Dir()上传目录
            self.upload_Dir(self.vtu_pagelist_path, filename)
        # 如果是文件 调用上传文件的方法
        elif filetype == _XFER_FILE:
            # 调用upload_file()上传文件
            self.upload_file(self.vtu_pagelist_path, filename)
        print("------------------vtu_pagelist文件上传完成------------------")

    def __filetype(self):
        """用来判断是文件还是目录"""
        if os.path.isfile(self.vtu_pagelist_path):
            # 判断路径字符串 是否为文件
            index = self.vtu_pagelist_path.rfind('\\')  # 通过rfind()方法 从右往左查找\ '\\'是需要转译没有查到就返回-1.这是windows路径的判断
            if index == -1:
                index = self.vtu_pagelist_path.rfind('/')  # 这是Linux路径的判断
            # 返回 标示和文件名称
            return (_XFER_FILE, self.vtu_pagelist_path[index + 1:])
        elif os.path.isdir(self.vtu_pagelist_path):
            # 判断路径字符串 是否为目录
            return (_XFER_DIR, "")  # 如果判断是目录返回标识和空的字符串

    def upload_Dir(self, localdir='./', remotedir='./'):
        """

        :param localdir: 本地文件路径
        :param remotedir: 文件名称  目录传过来的是“”字符串
        :return:
        """

        """上传文件夹"""
        # 如果不是目录就返回
        # print(localdir)
        if not os.path.isdir(localdir):
            return
        # 新建一个远程目录
        # 设置FTP当前操作的路径    "/sdcard/vtu_pagelist"
        self.ftp.cwd(os.path.join(self.vtu_pagelist_ftp_path, remotedir))

        self.vtu_pagelist_ftp_path = os.path.join(self.vtu_pagelist_ftp_path, remotedir)

        # print(self.vtu_pagelist_ftp_path)
        # 通过os.listdir()方法获取目录内的文件列表    "./vtu_config/vtu_pagelist"
        for file in os.listdir(localdir):
            # 通过os.path.join()方法做一个拼接，拼接成本地文件路径      ./vtu_config/vtu_pagelist/Equipment.files
            src = os.path.join(localdir, file)
            # print(src)
            # print(file)
            # # 拼接完成后 在判断是否为文件或者目录
            if os.path.isfile(src):
                self.upload_file(src, file)
            elif os.path.isdir(src):
                try:
                    # 在当前目录创建一个文件夹  因为之前cwd已经设置到了/sdcard/vtu_pagelist的当前路径
                    self.ftp.mkd(file)
                except:
                    sys.stderr.write("%s文件夹创建失败..." % file)
                self.upload_Dir(src, file)
        # 这一步是返回上一层菜单
        self.ftp.cwd('../')
        index = self.vtu_pagelist_ftp_path.rfind('\\')
        if index == -1:
            index = self.vtu_pagelist_ftp_path.rfind('/')
        self.vtu_pagelist_ftp_path = self.vtu_pagelist_ftp_path[0:index]
        # print(self.vtu_pagelist_ftp_path)

    def upload_file(self, localpath, remotepath='./'):
        """
        :param localpath: 本地文件路径
        :param remotepath: 文件名称
        :return:
        """
        # 在做一次判断 如果是目录直接return掉 不做操作
        if not os.path.isfile(localpath):
            return
        try:
            self.ftp.storbinary('STOR ' + os.path.join(self.vtu_pagelist_ftp_path, remotepath), open(localpath, 'rb'))
            print("文件%s上传到vtu_pagelist目录成功..." % remotepath)
        except:
            raise IOError("上传到vtu_pagelist目录错误...")

    def delete_vtu_pagelist_files(self):
        """
        思路1.直接删除整个文件夹rmd()然后新建cwd()文件夹，发现无法创建'_'带有下划线的目录（待解决）。pass
        思路2.列出目录列表然后通过抛出异常，rmd()来实现删除目录
        """
        self.ftp_connect()
        file_list = self.ftp.nlst(self.vtu_pagelist_ftp_path)
        if file_list != []:
            for file in file_list:
                # print(file)
                try:
                    self.ftp.delete(os.path.join(self.vtu_pagelist_ftp_path, file))
                    print('%s文件删除成功' % os.path.join(self.vtu_pagelist_ftp_path, file))
                except:
                    self.ftp.rmd(os.path.join(self.vtu_pagelist_ftp_path, file))
                    print('%s目录删除成功' % os.path.join(self.vtu_pagelist_ftp_path, file))
            print("------------------vtu_pagelist目录删除完成------------------")
        else:
            print("vtu_pagelist目录为空！")

    def delete_file(self):
        # 删除重启文件 重启机器
        self.ftp_connect()
        self.ftp.delete(self.reboot_path)
        self.ftp.quit()
        print("机器正在重启......")


if __name__ == "__main__":
    ftp_data = Ftp_Data()
    ftp_data.delete_vtu_pagelist_files()  # 先删除vtu_pagelist文件
    ftp_data.upload_vtu_pagelist_files()  # 再上传vtu_pagelist文件
    ftp_data.upload_SO_files()  # 上传so文件
    ftp_data.upload_XmlCfg_files()  # 上传xmlCfg文件
    ftp_data.delete_file()  # 删除boot文件  重启机器
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

# def try_error(self):
#     """
#     专门用来抛出错误，
#     """
#     print(self.vtu_pagelist_ftp_path)
# self.ftp.rmd(self.vtu_pagelist_ftp_path)
# self.ftp.mkd(self.vtu_pagelist_ftp_path)
# file_list = self.ftp.nlst(self.vtu_pagelist_ftp_path)
# print(file_list)
# """
# 没有优质的方法了，先满足需求再说
# 1、先cwd到文件目录，如果能进去就是目录，不能进去为文件直接delete
# 2、同样操作目录，然后返回上一层，rmd删除目录
#
# """
# # 新增目录列表
# # self.try_error(file_list)
# # 递归删除目录
# for file in file_list:
#     try:
#         self.ftp.delete(os.path.join(self.vtu_pagelist_ftp_path, file))
#         print('%s文件删除成功' % os.path.join(self.vtu_pagelist_ftp_path, file))
#     except:
#         self.vtu_pagelist_ftp_path = os.path.join(self.vtu_pagelist_ftp_path, file)
#         print(self.vtu_pagelist_ftp_path)
#         self.try_error()
# self.ftp.cwd('../')
# index = self.vtu_pagelist_ftp_path.rfind('\\')
# if index == -1:
#     index = self.vtu_pagelist_ftp_path.rfind('/')
# self.vtu_pagelist_ftp_path = self.vtu_pagelist_ftp_path[0:index]
# print(self.vtu_pagelist_ftp_path)
# self.ftp.rmd(file)
# print("删除%s文件成功..." % file)
