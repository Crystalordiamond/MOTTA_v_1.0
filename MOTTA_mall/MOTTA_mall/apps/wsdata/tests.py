from django.test import TestCase

# Create your tests here.


a = [1, 3, 4, 5, 76, 8, 6, 76, 5, 43453, 54, 54, 54, 43, 325, 5, 55, 5, 55, 2, 2, 45, 4545, 324]
print(len(a))
a1 = []
a2 = []
for index, value in enumerate(a):
    if index % 2 == 0:
        a1.append(value)
    else:
        a2.append(value)

nums = zip(a1, a2)
for i in nums:
    Hex_str = "".join('{:04x}'.format(x) for x in i)
    print(i)
    print(Hex_str)

alarm_list = [{"监控屏IO, 烟感": [{"烟雾告警": "0"}]},
              {"监控屏IO, 漏水": [{"漏水警告": "0"}]},
              {"温湿度, 温度": [{"高温告警": "40"}]},
              {"温湿度, 设备通讯状态": [{"设备通讯中断": "0"}]},
              {"UPS, 设备通讯状态": [{"设备通讯中断": "0"}]},
              {"主路电表, 设备通讯状态": [{"设备通讯中断": "0"}]},
              {"IT负载电表, 设备通讯状态": [{"设备通讯中断": "0"}]},
              {"空调, 设备通讯状态": [{"设备通讯中断": "0"}]}]

# print([key for key, value in (i for i in alarm_list).items()])

for i in alarm_list:
    for key, value in i.items():
        for a, b in value[0].items():
            print(a)


import copy

data = [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1]
time = ["2019-06-18 12:02:01", "2019-06-18 12:02:02", "2019-06-18 12:02:03", "2019-06-18 12:02:04",
        "2019-06-18 12:02:05", "2019-06-18 12:02:06", "2019-06-18 12:02:07", "2019-06-18 12:02:08",
        "2019-06-18 12:02:09", "2019-06-18 12:02:12", "2019-06-18 12:02:13", "2019-06-18 12:02:14"
        ]
start = []
end = []
dict = []
flag = 0
n = len(data)
i = 0
while i < n:
    if data[i] == 0 and flag == 0:
        flag = 1
        dict.append(data[i])
        start.append(time[i])
    if data[i] == 1 and flag == 1:
        flag = 0
        dict.append(data[i])
        end.append(time[i])
    i += 1

# print(dict)
# print(start)
# print(end)

n = [
    {"id": 1, "data": 0, "time": 2132144},
    {"id": 2, "data": 1, "time": 2132144},
    {"id": 3, "data": 1, "time": 2132144},
    {"id": 4, "data": 1, "time": 2132144},
    {"id": 5, "data": 0, "time": 2132144},
    {"id": 6, "data": 0, "time": 2132144},
    {"id": 7, "data": 0, "time": 2132144},
    {"id": 8, "data": 1, "time": 2132144},
    {"id": 9, "data": 0, "time": 2132144},
    {"id": 10, "data": 0, "time": 2132144},
    {"id": 11, "data": 0, "time": 2132144},
    {"id": 12, "data": 0, "time": 2132144},
    {"id": 13, "data": 1, "time": 2132144},
]

all_list = []
start_end = []
flag = True
for index, i in enumerate(n):
    if flag and i["data"] == 0:
        start_end.append(i)
        flag = False
    if not flag and i["data"] == 1:
        start_end.append(i)
        flag = True
    if index == (len(n) - 1) and n[len(n) - 1]["data"] == 0:
        n[index]["time"] = None
        start_end.append(n[index])
    if len(start_end) == 2:
        emp = copy.copy(start_end)
        all_list.append(emp)
        start_end = []

print(all_list)
