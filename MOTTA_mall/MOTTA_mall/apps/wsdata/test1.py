list = [

    {"监控屏IO": [
        {"监控屏IO, 烟感": ["烟雾告警", "有告警", "严重告警", "-", 1], "max_id": None},
        {"监控屏IO, 漏水": ["漏水告警", "有告警", "严重告警", "-", 1]},
        {"监控屏IO, 机柜门": ["机柜门", "打开", "一般告警", "-", 1]},
        {"监控屏IO, 通讯状态": ["设备通讯状态", "通讯中断", "一般告警", "-", 1]}]},

    {"温湿度": [
        {"温湿度, 温度": ["高温告警", "有告警", "严重告警", "℃", 41]},
        {"温湿度, 温度": ["低温告警", "有告警", "一般告警", "℃", 10]},
        {"温湿度, 湿度": ["高湿告警", "有告警", "一般告警", "%Rh", 95]},
        {"温湿度, 湿度": ["低湿告警", "有告警", "一般告警", "%Rh", 10]},
        {"温湿度, 设备通讯状态": ["设备通讯状态", "通讯中断", "严重告警", "-", 1]}
    ]},


]
a = {"max1_id": None, "max2_id": None}  # 定义一个全局变量 有浮动变化的数字
flag = 0  # 0 1变量

list_data = []
# 获取模块的字典对象[{"监控屏IO":[{},{},{},...]},...,...]
for item in list:
    # 获取模块名称"equipment=监控屏IO"，及模块里面的设备列表value = [{"监控屏IO, 烟感": ["烟雾告警", "有告警", "严重告警", "-", 1]},{...},{...},...]
    for equipment, value in item.items():
        # 获得字典对象
        print(equipment)
        print(value)
        for value_list in value:
            print(value_list)

li = "abcdefg"
print(li[-3:])

print(li[:5])