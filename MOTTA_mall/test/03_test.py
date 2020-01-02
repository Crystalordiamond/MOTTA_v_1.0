# import datetime
# abs = "2019-11-27 16:15:32"
# aaaa = datetime.datetime.strptime(abs, "%Y-%m-%d %H:%M:%S")
# # print(datetime.datetime.strptime("00:59:00", "%Y-%m-%d %H:%M:%S"))
# time_data = datetime.datetime.strptime("2019-11-27 16:16:32", "%Y-%m-%d %H:%M:%S")
# if time_data - aaaa > datetime.timedelta(days=1/24/60/10):
#     print(time_data - aaaa)
#     print(datetime.timedelta(days=1/24/60/60))
import re

zm = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

adict = [{"地面漏水/溢水 ": " Water Leakage/Over Alarm"},
         {"加热器过载": "Heater Alarm"},
         {"高压开关/排气温度过高开关 ": " HP/HD Switch"},
         {"过滤网压差开关": "Filter Maintenance"},
         {"室内AC风机启停": "ID Fan Status"},
         {"定频压缩机启停": "Fix Compressor Status"},
         {"加热器启停": "Heater Status"},
         {"加湿器启停": "Humidifier Status"},
         {"旁通电磁阀启停": "Bypass Valve Status"},
         {"低温电磁阀": "Lee Valve Status"},
         {"地面漏水/溢水 ": " Leakage/Over Water"},
         {"加热器过载": "Heater Fault"},
         {"高压/排气开关 ": " HP/HD Switch Alarm"},
         {"过滤网堵塞": "Filter Maintenance"},
         {"吸气压力传感器故障": "Suction Pressure Sensor Failure"},
         {"排气压力传感器故障": "Discharge Pressure Sensor Failure"},
         {"吸气温度传感器故障": "Suction Temperature Sensor Failure"},
         {"送风温度传感器故障": "Supply Temperature Sensor Failure"},
         {"回风温度传感器故障": "Return Temperature Sensor Failure"},
         {"回风湿度传感器故障": "Return Humidity Sensor Failure"},
         {"液管温度传感器故障": "Liquid Pipe Temperature Sensor Failure"},
         {"排气压力过高告警": "High Pressure Alarm"},
         {"吸气压力过低告警": "Low Pressure Alarm"},
         {"高温告警": "High Temperature Alarm"},
         {"低温告警": "Low Temperature Alarm"},
         {"高湿告警": "High Humidity Alarm"},
         {"低湿告警": "Low Humidity Alarm"},
         {"控制器变量故障": "Controller Variable Alarm"},
         {"主机与从机1通讯故障": "Communication Alarm with Slave unit1"},
         {"主机与从机2通讯故障": "Communication Alarm with Slave unit2"},
         {"主机与从机3通讯故障": "Communication Alarm with Slave unit3"},
         {"主机与从机4通讯故障": "Communication Alarm with Slave unit4"},
         {"主机与从机5通讯故障": "Communication Alarm with Slave unit5"},
         {"主机与从机6通讯故障": "Communication Alarm with Slave unit6"},
         {"主机与从机7通讯故障": "Communication Alarm with Slave unit7"},
         {"主机与从机8通讯故障": "Communication Alarm with Slave unit8"},
         {"EEV 范围误差": "Range error"},
         {"EEV 低过热度": "Low Superheat"},
         {"EEV 低蒸发温度": "Low Evaporation Temperature"},
         {"EEV 高蒸发温度": "High Evaporation Temperature"},
         {"EEV 高冷凝温度": "High Condense Temperature"},
         {"EEV 低吸气温度": "Low Suction Temperature"},
         {"EEV 电机故障": "Motor error"},
         {"EEV 自适应控制无效": "Invalid Adaptive Control"},
         {"EEV 紧急关闭": "Emergency OFF"},
         {"EEV 阀ID错误": "Valve ID Wrong"},
         {"EEV 传感器位置错误": "Sensor Position Wrong"},
         {"EEV 传感器量程错误": "Sensor Range Wrong"},
         {"CPY通讯离线": "CPY Communication Alarm"},
         {"模块预维护时间告警": "Module Maintenance Alarm"},
         {"室内风机预维护时间告警": "ID Fan Maintenance Time"},
         {"压缩机预维护时间告警": "Compressor Maintenance Time"},
         {"室外机预维护时间告警": "OD Fan Maintenance Time"},
         {"加湿器预维护时间告警": "Humidifier Maintenance Time"},
         {"吸气压力": "LP Pres"},
         {"排气压力": "HP Pres"},
         {"吸气温度": "Suction Temp"},
         {"送风温度": "Supply Temp"},
         {"回风温度": "Return Temp"},
         {"回风湿度": "Humidity"},
         {"液管温度": "Liquid Pipe Temp"},
         {"过冷度": "Subcooling"},
         {"室内EC风机转速": " ID Fan Speed"},
         {"压缩机变频器转速": "Compressor Output"},
         {"室外机EC风机转速/室外变频器转速 ": " OD Fan Speed"},
         {"过热度": "Superheat"},
         {"电子膨胀阀步数": "EEV Step"},
         {"电子膨胀阀开度": "EEV Open Percent"},
         {"机组工作状态": " Unit Mode"},
         {"室内风机运行时间": "ID Fan Running Time"},
         {"压缩机运行时间": "Comp Running Time"},
         {"运行模式选择": "Manual Control"},
         {"开/关机 ": " ON-OFF"},
         {"启动延时": "Repower Auto-ON DT"},
         {"运行时间清除": "Runing Time Reset"},
         {"手动清除报警": "Clear Alarm"},
         {"恢复工厂设置": "Factory Reset"},
         {"制冷温度设置": "Temp Setting"},
         {"制冷温度比例带设置": "Temp Band"},
         {"压缩机最小输出转速": "Min Freq"},
         {"压缩机最大输出转速": "Max Freq"},
         {"回油开始频率": "Oil Start Speed"},
         {"回油间隔时间": "Oil Interval Time"},
         {"回油运行时间": "Oil Running Time"},
         {"最低送风温度": "Min Supply Temp"},
         {"最高送风温度": "Max Supply Temp"},
         {"压缩机延时启动": "Trun On Comp DT"},
         {"冷媒型号": "Refrigerant"},
         {"预留": "Reserved"},
         {"除湿限制温度": "Dehum Limit Temp"},
         {"湿度设定": "Humid Setting"},
         {"湿度偏差设定": "Humid Band"},
         {"加热启动判断延时": "Heating Judge Time"},
         {"高温报警阙值设置": "High Temp Alarm Band"},
         {"低温报警阙值设置": "Low Temp Alarm Band"},
         {"高湿报警阙值设置": "High Humid Alarm Band"},
         {"低湿报警阙值设置": "Low Humid Alarm Band"},
         {"吸气压力过低设置": "LP Pres Alarm"},
         {"吸气压力过低恢复设置": "LP Pres Recov"},
         {"压缩机启动后延时(用于低压检测)": "LP DT Setting"},
         {"吸气压力过低延时": "LP Alarm Time"},
         {"排气压力过高设置": "HP Pres Alarm"},
         {"排气压力过高恢复设置": "HP Pres Recov"},
         {"室内EC风机 最大变化率": "ID Fan Speed CR"},
         {"室内风机 停机延时": "Trun Off DT"},
         {"室内风机 最小转速设置": "ID Fan Min Speed"},
         {"室内风机 最大转速设置": "ID Fan Max Speed"},
         {"除湿时室内风机转速设置": "Dehum Fan Speed"},
         {"冷凝风机  最大变化率": "OD Fan Speed CR"},
         {"冷凝风机  最小转速设置": "OD Fan Min Speed"},
         {"冷凝风机  最大转速设置": "OD Fan Max Speed"},
         {"冷凝风机  启动压力": "Fan Pres Setting"},
         {"冷凝风机  启动偏差": "Fan Pres Band"},
         {"机组运行时间": "Unit Running Time"},
         {"冷凝风机运行时间": "OD Fan Running Time"},
         {"加湿器运行时间高字节": "Humid Running Time"},
         {"加湿器运行时间": "Humid Running Time"},
         {"自动": "Auto"},
         {"手动": "Manual "},
         {"待机": "Standby"},
         {"加湿": "Hum"},
         {"制冷+加湿": " Cooling&Hum"},
         {"闭合": "Close"},
         {"断开": "Open"},
         {"关闭": "OFF"},
         {"开启": "ON"},
         {"正常": "Normal"},
         {"告警": "Alarm"},
         {"除湿": "Dehum"},
         {"制冷": "Cooling"}]
# python中 chr(数字) 会将转换为ascii码对应的字符，ord()则相反。
# for letter in range(65,91):
#      print(chr(letter))

file_data = ''
for item in adict:
    # print(item)
    for i in item:
        # print(i)
        # print(item[i])
        for index, j in enumerate(item[i]):
            if index == 0 and j == ' ':
                # print(item[i][1:])
                item[i] = item[i][1:]

    with open('./ATTOM.xml', 'r', encoding="utf-8") as f:
        for line in f:
            for h in item:
                # print(h)
                # print(item[h])
                if item[h] in line:
                    ss = line.replace(item[h], h)

                    file_data += ss
    with open('./ATTOM11.xml', 'w', encoding="utf-8") as f:
        f.write(file_data)
