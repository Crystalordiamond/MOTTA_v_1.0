# 定义的名称根据map表取值
# 温度
temps = [{"sigid": "1", "name": "Temp-Humidity, Temperature"}]
# 湿度
Humidity = [{"sigid": "2", "name": "Temp-Humidity, Humidity"}]
# 输入电压
input_vol = [{"sigid": "1", "name": "UPS, RatingInputVoltage"}, {"sigid": "1", "name": "UPS, InputVoltage"}]
# 输出电压
output_vol = [{"sigid": "3", "name": "UPS, RatingOutputVoltage"}, {"sigid": "3", "name": "UPS, OutputVoltage"}]
# 输入频率
input_fre = [{"sigid": "2", "name": "UPS, RatingInputFrequency"}, {"sigid": "2", "name": "UPS, InputFrequency"}]
# 输出频率
output_fre = [{"sigid": "4", "name": "UPS, RatingOutputFrequency"}, {"sigid": "4", "name": "UPS, OutputFrequency"}]
# 输入相序
input_phase = [{"sigid": "31", "name": "UPS, InputPhases"}, {"sigid": "191", "name": "UPS, InputPhase"}]
# 输出相序
output_phase = [{"sigid": "46", "name": "UPS, OutputPhases"}, {"sigid": "192", "name": "UPS, OutputPhase"}]
# 电表功率
meter_power = [{"sigid": "6", "name": "Primary Meter, Power"},
               {"sigid": "11", "name": "Primary Meter, Phase 1 active power"}]
# ups负载率
ups_load = [{"sigid": "50", "name": "UPS, OutputLoad1"}, {"sigid": "6", "name": "UPS, OutputLoad"}]

# 空调回风温度
Return_Temp = [{"sigid": "87", "name": "Air Conditioner, Return Temp"},
               {"sigid": "66", "name": "Air Conditioner, IndoorTemp"}, ]
# 空调送风温度
Discharge_Temp = [{"sigid": "86", "name": "Air Conditioner, Supply Temp"},
                  {"sigid": "63", "name": "Air Conditioner, OutletTemp"}, ]
# 空调湿度
AC_Humidity = [{"sigid": "88", "name": "Air Conditioner, Humidity"},
               {"sigid": "67", "name": "Air Conditioner, IndoorHumidity"}, ]
# 空调状态
AC_Mode = [{"sigid": "97", "name": "Air Conditioner, Unit Mode"},{"sigid": "37", "name": "Air Conditioner, RunningStatus"}, ]
# 漏水
Leaking = [{"sigid": "2", "name": "VTU-IO, Leakage"}, ]
# Ups信号值
UPS_Signal = [{"sigid": "201", "name": "UPS, UPSSimplifyMode"}, {"sigid": "100", "name": "UPS, UPS Simplify Mode"}]

