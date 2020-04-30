# 定义的名称根据map表取值

# 1.ups 协议的类型名称 UPS_6-10K.so--日月元--232, UPS_INVT_X7-20.so--英威腾--485, UPS-GXT4.so--Vertiv--485
# 这里的名称要与配置工具中so文件名称一致UPS_GXT4.so(UPS-GXT4.so)避免混淆
ups_type = ["UPS_6-10K.so", "UPS_INVT_X7-20.so", "UPS_GXT4.so"]
# 输入电压，输出电压，输入频率，输出频率，输入电流(没有)，输出电流，运行模式（取的是Singal表对应的数据） ups的负载率
RYY = [{"sigid": "1", "name": "InputVoltage"}, {"sigid": "3", "name": "OutputVoltage"},
       {"sigid": "2", "name": "InputFrequency"}, {"sigid": "4", "name": "OutputFrequency"},
       {"sigid": "5", "name": "OutputCurrent"}, {"sigid": "201", "name": "UPSSimplifyMode"},
       {"sigid": "6", "name": "OutputLoad"}]
# 输入电压，输入频率,输入电流,输出电压，输出频率，输出电流 ups工作模式
VERTIV = [{"sigid": "34", "name": "System Input RMS L1-L2"}, {"sigid": "37", "name": "System Input Frequency"},
          {"sigid": "43", "name": "System Input Nominal Current"},
          {"sigid": "70", "name": "System Output Voltage RMS L1-L2"},
          {"sigid": "74", "name": "System Output Frequency"},
          {"sigid": "73", "name": "System Output RMS Current L2"},
          {"sigid": "73", "name": "Simplified UPS mode"},
          {"sigid": "82", "name": "System Output Pct Power"}]

# 2. 温湿度目前只有一种协议
TH_type = ["THSE10.so"]
# 温度,湿度
TempsHumidity = [{"sigid": "1", "name": "Temperature"}, {"sigid": "2", "name": "Humidity"}]

# 3. YD2010C-K-V.so--d大电表， DDS3366D-1P.so--小电表
Meter_type = ["YD2010C-K-V.so", "DDS3366D-1P.so"]
#  电压、电流、功率（Frequency）、功率因素、总能耗（A B C三相“Negative active energy&#xA;&#xA;” ） 仪表盘显示的总功率
B_meter = [{"sigid": "8", "name": "Phase voltage1"}, {"sigid": "10", "name": "Phase 1 current"},
           {"sigid": "11", "name": "Phase 1 active power"}, {"sigid": "12", "name": "Phase 1 power factor"},
           {"sigid": "15", "name": "Phase voltage2"}, {"sigid": "17", "name": "Phase 2 current"},
           {"sigid": "18", "name": "Phase 2 active power"}, {"sigid": "19", "name": "Phase 2 power factor"},
           {"sigid": "22", "name": "Phase voltage3"}, {"sigid": "24", "name": "Phase 3 current"},
           {"sigid": "26", "name": "Phase 3 active power"}, {"sigid": "27", "name": "Phase 3 power factor"},
           {"sigid": "33", "name": "Frequency"},
           {"sigid": "40", "name": "Negative active energy&#xA;&#xA;"},
           {"sigid": "34", "name": "Three phase active power"}]

# 电压、电流、功率、功率因素、总能耗
L_meter = [{"sigid": "4", "name": "Voltage"}, {"sigid": "5", "name": "Current"},
           {"sigid": "8", "name": "Frequency"}, {"sigid": "6", "name": "Power"},
           {"sigid": "7", "name": "PowerFactor"}, {"sigid": "1", "name": "TotalActiveEnergy"}]

# 4.空调 SmoothAir_Carel_DX.so--卡乐
AC_type = ["SmoothAir_Carel_DX.so", "SL1600F_FC.so"]
# 送风温度，回风温度，湿度，工作模式
AC_KL = [{"sigid": "86", "name": "Supply Temp"}, {"sigid": "85", "name": "Suction Temp"},
         {"sigid": "88", "name": "Humidity"}, {"sigid": "75", "name": "Control Mode"},
         {"sigid": "23", "name": "Leakage/Over Water"}]

AC_SL = [{"sigid": "62", "name": "InletTemp"}, {"sigid": "63", "name": "OutletTemp"},
         {"sigid": "67", "name": "IndoorHumidity"}, {"sigid": "46", "name": "ControlMode"},
         {"sigid": "31", "name": "Leakage"}]

# 5.vtu
VTU_type = ["VTUIO.so"]
# 烟感，漏水，门状态
VTU = [{"sigid": "1", "name": "Smoke"}, {"sigid": "2", "name": "Leakage"},
       {"sigid": "3", "name": "Door"}]
