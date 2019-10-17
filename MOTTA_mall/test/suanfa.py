""""""
def a():
    print('111111')

#
# def sum(arg):
#     b = []
#     for list in a:
#         print(list)
#
#         for x in list:
#             b.append(x)
#     print(b)
#     # while b:
#     if arg in b:
#         return True
#     else:
#         return False
#
#
# # sum(50)
# print("--------------------")
# print(sum(50))
"""
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

示例:

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
"""


class Solution(object):
    def twoSum(self, num, list):
        for num1 in range(len(list)):
            for num2 in range(num1 + 1, len(list)):
                if list[num1] + list[num2] == num:
                    return num1, num2


num = Solution()
n = num.twoSum(8, [2, 3, 4, 5, 6, 7])
print(n)
import sys
import os
import json
from ftplib import FTP

_XFER_FILE = 'FILE'
_XFER_DIR = 'DIR'


class Xfer(object):
    '''''
    @note: upload local file or dirs recursively to ftp server
    '''

    def __init__(self):
        self.ftp = None

    def __del__(self):
        pass

    def setFtpParams(self, ip, uname, pwd, port=21, timeout=60):
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = port
        self.timeout = timeout

    def initEnv(self):
        if self.ftp is None:
            self.ftp = FTP()

            print('### connect ftp server: %s ...' % self.ip)
            self.ftp.connect(self.ip, self.port, self.timeout)
            self.ftp.login(self.uname, self.pwd)

            print(self.ftp.getwelcome())

    def clearEnv(self):
        if self.ftp:
            self.ftp.close()
            print('### disconnect ftp server: %s!' % self.ip)
            self.ftp = None

    def uploadDir(self, localdir='./', remotedir='./'):
        if not os.path.isdir(localdir):
            return
        # 设置FTP当前操作的路径
        # self.ftp.cwd(remotedir)
        for file in os.listdir(localdir):
            # os.path.join(localdir, file) 拼接字符串的用法，这里把./和so拼接到了一起
            src = os.path.join(localdir, file)
            print(src)
            if os.path.isfile(src):
                self.uploadFile(src, file)
            elif os.path.isdir(src):
                try:
                    self.ftp.mkd(file)
                    pass
                except:
                    sys.stderr.write('the dir is exists %s' % file)
                self.uploadDir(src, file)
        self.ftp.cwd('..')

    def uploadFile(self, localpath, remotepath='./'):
        if not os.path.isfile(localpath):
            print(os.path.isfile(localpath))
            return
        print('+++ upload %s to :%s' % (localpath, remotepath))
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))

    def __filetype(self, src):
        if os.path.isfile(src):
            # Python rfind()返回字符串最后一次出现的位置(从右向左查询)，如果没有匹配项则返回 - 1。
            index = src.rfind('\\')
            if index == -1:
                index = src.rfind('/')
            # print(index)
            # print(_XFER_FILE)
            # print(src[index + 1:])
            return _XFER_FILE, src[index + 1:]
        elif os.path.isdir(src):
            return (_XFER_DIR, '')

    def upload(self, src):
        filetype, filename = self.__filetype(src)
        # 连接ftp
        # self.initEnv()

        # 做判断 是文件还是文件夹
        if filetype == _XFER_DIR:
            print(1)
            self.srcDir = src
            # 文件夹就跳转
            print(self.srcDir)
            self.uploadDir(self.srcDir)
        elif filetype == _XFER_FILE:

            self.uploadFile(src, filename)
        self.clearEnv()


if __name__ == '__main__':
    srcDir = "./vtu_config/sampler/SO"
    srcFile = r'C:\sytst\sar.c'
    xfer = Xfer()
    # xfer.setFtpParams('192.x.x.x', 'jenkins', 'pass')
    xfer.upload(srcDir)
    # xfer.upload(srcFile)
