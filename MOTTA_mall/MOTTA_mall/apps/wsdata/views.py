# -*- coding: utf-8 -*-
from xmldata.models import XmlData
from createdata.models import EquipmentData
from warning.models import Warning
from divices.models import divices
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import json
import time
from django.db.models import Q, F

# 告警列表
list_war = [

    {"监控屏IO": [
        {"监控屏IO, 烟感": ["烟雾告警", "有告警", "严重告警", "-", 1, {"max_id": 0}]},
        {"监控屏IO, 漏水": ["漏水告警", "有告警", "严重告警", "-", 1, {"max_id": 0}]},
        {"监控屏IO, 机柜门": ["机柜门", "打开", "一般告警", "-", 0, {"max_id": 0}]},
        {"监控屏IO, 通讯状态": ["设备通讯状态", "通讯中断", "一般告警", "-", 1, {"max_id": 0}]}]},

    {"温湿度": [
        {"温湿度, 温度": ["高温告警", "有告警", "严重告警", "℃", 41, {"max_id": 0}]},
        {"温湿度, 温度": ["低温告警", "有告警", "一般告警", "℃", 10, {"max_id": 0}]},
        {"温湿度, 湿度": ["高湿告警", "有告警", "一般告警", "%Rh", 95, {"max_id": 0}]},
        {"温湿度, 湿度": ["低湿告警", "有告警", "一般告警", "%Rh", 10, {"max_id": 0}]},
        {"温湿度, 设备通讯状态": ["设备通讯状态", "通讯中断", "严重告警", "-", 1, {"max_id": 0}]}
    ]},

    {"UPS": [
        {"UPS, 市电异常": ["市电异常", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 旁路/逆变": ["旁路/逆变", "有效", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, UPS故障": ["UPS故障", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, EPO": ["EPO", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 测试状态": ["测试状态", "测试中", "通知", "-", 1, {"max_id": 0}]},
        {"UPS, 关机有效": ["关机有效", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 电池测试失败": ["电池测试失败", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 电池未接": ["电池未接", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 电池过充": ["电池过充", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 电池低压": ["电池低压", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 输出过载": ["输出过载", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 风扇堵转": ["风扇堵转", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 过温": ["过温", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 充电器故障": ["充电器故障", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, L1输入保险开路": ["L1输入保险开路报警", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 维护开关盖打开": ["维护开关盖打开", "有告警", "一般告警", "-", 1, {"max_id": 0}]},
        {"UPS, 设备通讯状态": ["设备通讯状态", "通讯中断", "严重告警", "-", 1, {"max_id": 0}]}]},
    {"主路电表": [
        {"主路电表, 设备通讯状态": ["设备通讯状态", "通讯中断", "严重告警", "-", 1, {"max_id": 0}]}]},
    {"IT负载电表": [
        {"IT负载电表, 设备通讯状态": ["设备通讯状态", "通讯中断", "严重告警", "-", 1, {"max_id": 0}]}]},
    {"空调": [
        {"空调, 吸气温度探头故障": ["吸气温度探头故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 送风温度探头故障": ["送风温度探头故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 吸气压力探头故障": ["吸气压力探头故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 排气压力探头故障": ["排气压力探头故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 回风温度探头故障": ["回风温度探头故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 回风湿度探头故障": ["回风湿度探头故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 温度过高": ["温度过高", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 送风温度过低": ["送风温度过低", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 湿度过高": ["湿度过高", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 湿度过低": ["湿度过低", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 水溢报警": ["水溢报警", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 漏水报警": ["漏水报警", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 高压保护开关": ["高压保护开关", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 低压保护开关": ["低压保护开关", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 烟雾报警": ["烟雾报警", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 送风机故障": ["送风机故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 加湿器故障": ["加湿器故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 电加热故障": ["电加热故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 水泵故障": ["水泵故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 低压压力报警": ["低压压力报警", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 电流过载": ["电流过载", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 排气压力过高报警": ["排气压力过高报警", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 压缩机内部故障": ["压缩机内部故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        {"空调, 压缩机通讯故障": ["通讯故障", "故障", "一般告警", "-", 1, {"max_id": 0}]},
        # {"空调, 压缩机高压保护": ["压缩机高压保护", "告警", "一般告警", 1]},
        # {"空调, 压缩机低压保护": ["压缩机低压保护", "告警", "一般告警", 1]},
        {"空调, 设备通讯状态": ["设备通讯状态", "通讯中断", "严重告警", "-", 1, {"max_id": 0}]}]}
]
# 历史数据列表
list_eq = [

    {"监控屏IO": [
        {"监控屏IO, 烟感": [{"name": "烟感", "unit": "-", "0": "告警", "1": "正常", "max_id": 0}]},
        {"监控屏IO, 漏水": [{"name": "漏水", "unit": "-", "0": "告警", "1": "正常", "max_id": 0}]},
        {"监控屏IO, 机柜门": [{"name": "机柜门", "unit": "-", "0": "关闭", "1": "打开", "max_id": 0}]},
        {"监控屏IO, DI4": [{"name": "DI4", "unit": "-", "0": "有输入", "1": "无输入", "max_id": 0}]},
        {"监控屏IO, DI5": [{"name": "DI5", "unit": "-", "0": "有输入", "1": "无输入", "max_id": 0}]},
        {"监控屏IO, 通讯状态": [{"name": "通讯状态", "unit": "-", "0": "中断", "1": "正常", "max_id": 0}]}]},
    {"温湿度": [
        {"温湿度, 温度": [{"name": "温度", "unit": "℃", "max_id": 0}]},
        {"温湿度, 湿度": [{"name": "湿度", "unit": "%Rh", "max_id": 0}]},
        {"温湿度, 门开启温度": [{"name": "门开启温度", "unit": "℃", "max_id": 0}]},
        {"温湿度, 门关闭温度": [{"name": "门关闭温度", "unit": "℃", "max_id": 0}]},
        {"温湿度, 设备通讯状态": [{"name": "设备通讯状态", "unit": "-", "0": "中断", "1": "正常", "max_id": 0}]}]},
    {"UPS": [
        {"UPS, 输入电压": [{"name": "输入电压", "unit": "V", "max_id": 0}]},
        {"UPS, 输入频率": [{"name": "输入频率", "unit": "Hz", "max_id": 0}]},
        {"UPS, 输出电压": [{"name": "输出电压", "unit": "V", "max_id": 0}]},
        {"UPS, 输出频率": [{"name": "输出频率", "unit": "Hz", "max_id": 0}]},
        {"UPS, 输出电流": [{"name": "输出电流", "unit": "A", "max_id": 0}]},
        {"UPS, 输出负载率": [{"name": "输出负载率", "unit": "%", "max_id": 0}]},
        {"UPS, 正母线电压": [{"name": "正母线电压", "unit": "V", "max_id": 0}]},
        {"UPS, 负母线电压": [{"name": "负母线电压", "unit": "V", "max_id": 0}]},
        {"UPS, 电池电压": [{"name": "电池电压", "unit": "V", "max_id": 0}]},
        {"UPS, 最大检测温度": [{"name": "最大检测温度", "unit": "℃", "max_id": 0}]},
        {"UPS, UPS类型": [{"name": "UPS类型", "unit": "-", "0": "后备式", "1": "在线互动式", "10": "在线式", "max_id": 0}]},
        {"UPS, 市电异常": [{"name": "市电异常", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 电池低压": [{"name": "电池低压", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 旁路/逆变": [{"name": "旁路/逆变", "unit": "-", "0": "正常", "1": "有效", "max_id": 0}]},
        {"UPS, UPS故障": [{"name": "UPS故障", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, EPO": [{"name": "EPO", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 测试状态": [{"name": "测试状态", "unit": "-", "0": "非测试", "1": "测试中", "max_id": 0}]},
        {"UPS, 关机有效": [{"name": "关机有效", "unit": "-", "0": "正常", "1": "关机", "max_id": 0}]},
        {"UPS, 电池静音": [{"name": "电池静音", "unit": "-", "0": "非静音", "1": "静音", "max_id": 0}]},
        {"UPS, 电池测试失败": [{"name": "电池测试失败", "unit": "-", "0": "无", "1": "失败", "max_id": 0}]},
        {"UPS, 电池测试正常": [{"name": "电池测试正常", "unit": "-", "0": "无", "1": "正常", "max_id": 0}]},
        {"UPS, 电池未接": [{"name": "电池未接", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 电池过充": [{"name": "电池过充", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 电池低压": [{"name": "电池低压", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 输出过载": [{"name": "输出过载", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 风扇堵转": [{"name": "风扇堵转", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, EPO激活": [{"name": "EPO激活", "unit": "-", "0": "无效", "1": "生效", "max_id": 0}]},
        {"UPS, 过温": [{"name": "过温", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 充电器故障": [{"name": "充电器故障", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, L1输入保险开路": [{"name": "L1输入保险开路", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, 维护开关盖打开": [{"name": "维护开关盖打开", "unit": "-", "0": "正常", "1": "告警", "max_id": 0}]},
        {"UPS, UPS模式": [
            {"name": "UPS模式", "unit": "-", "80": "开机", "83": "待机", "89": "旁路", "76": "Line", "66": "电池供电", "84": "电池测试",
             "70": "故障", "69": "HE/ECO", "67": "Converter", "68": "关机", "max_id": 0}]},
        {"UPS, 电池电压": [{"name": "电池电压", "unit": "V", "max_id": 0}]},
        {"UPS, 电池节数": [{"name": "电池节数", "unit": "-", "max_id": 0}]},
        {"UPS, 电池组数": [{"name": "电池组数", "unit": "-", "max_id": 0}]},
        {"UPS, 电池容量": [{"name": "电池容量", "unit": "%", "max_id": 0}]},
        {"UPS, 电池剩余时间": [{"name": "电池剩余时间", "unit": "min", "max_id": 0}]},
        {"UPS, 输出功率因素": [{"name": "输出功率因素", "unit": "-", "max_id": 0}]},
        {"UPS, 输入相数": [{"name": "输入相数", "unit": "-", "max_id": 0}]},
        {"UPS, 输出相数": [{"name": "输出相数", "unit": "-", "max_id": 0}]},
        {"UPS, 输入故障电压": [{"name": "输入故障电压", "unit": "V", "max_id": 0}]},
        {"UPS, 输出故障电压": [{"name": "输出故障电压", "unit": "V", "max_id": 0}]},
        {"UPS, 额定电池节数": [{"name": "额定电池节数", "unit": "-", "max_id": 0}]},
        {"UPS, 额定电池单体电压": [{"name": "额定电池单体电压", "unit": "V", "max_id": 0}]},
        {"UPS, 错误码": [
            {"name": "错误码", "unit": "-", "0": "无故障", "1": "BUS电压启动失败", "2": "BUS电压过高", "3": "BUS电压过低", "4": "BUS电压不平衡",
             "5": "BUS电压下降斜率过快", "6": "PFC输入电感电流过大", "17": "Inverter软启动失败", "18": "Inverter电压过高", "19": "Inverter电压过低",
             "20": "L1 Inverter短路", "21": "L2 Inverter短路", "22": "L3 Inverter短路", "23": "L1L2 Inverter短路",
             "24": "L2L3 Inverter短路", "25": "L3L1 Inverter短路", "26": "L1 Inverter负功率超范围", "27": "L2 Inverter负功率超范围",
             "28": "L3 Inverter负功率超范围", "33": "电池SCR故障", "34": "Line SCR故障", "35": "Inverter继电器开路故障",
             "36": "Inverter继电器短路故障", "37": "输入输出线路接反", "38": "电池反接故障", "39": "电池电压过高", "40": "电池电压过低",
             "41": "电池FUSE开路故障", "49": "CANBus通讯故障", "50": "主机信号线路故障", "51": "同步信号线路故障", "52": "同步触发信号线路故障",
             "53": "并机通信线路丢失故障", "54": "输出严重不均流故障", "65": "温度过高", "66": "控制板中CPU间通讯故障", "67": "过载故障", "68": "风扇模组故障",
             "69": "充电器故障", "70": "机型错误", "71": "控制板与通讯板MCU通讯故障", "max_id": 0}]},
        {"UPS, UPS简化模式": [
            {"name": "UPS简化模式", "unit": "-", "0": "待机/关机", "1": "旁路", "2": "市电", "3": "电池", "max_id": 0}]},
        {"UPS, 设备通讯状态": [{"name": "设备通讯状态", "unit": "-", "0": "通讯中断", "1": "通讯正常", "max_id": 0}]}]},
    {"主路电表": [
        {"主路电表, 当前组合有功电能": [{"name": "当前组合有功电能", "unit": "Kwh", "max_id": 0}]},
        {"主路电表, 当前正向有功电能": [{"name": "当前正向有功电能", "unit": "Kwh", "max_id": 0}]},
        {"主路电表, 当前反向有功电能": [{"name": "当前反向有功电能", "unit": "Kwh", "max_id": 0}]},
        {"主路电表, 电压": [{"name": "电压", "unit": "V", "max_id": 0}]},
        {"主路电表, 电流": [{"name": "电流", "unit": "A", "max_id": 0}]},
        {"主路电表, 功率": [{"name": "功率", "unit": "Kw", "max_id": 0}]},
        {"主路电表, 功率因数": [{"name": "功率因数", "unit": "-", "max_id": 0}]},
        {"主路电表, 频率": [{"name": "频率", "unit": "Hz", "max_id": 0}]},
        {"主路电表, 设备通讯状态": [{"name": "设备通讯状态", "unit": "-", "0": "通讯中断", "1": "通讯正常", "max_id": 0}]}]},
    {"IT负载电表": [
        {"主路电表, 当前组合有功电能": [{"name": "当前组合有功电能", "unit": "Kwh", "max_id": 0}]},
        {"主路电表, 当前正向有功电能": [{"name": "当前正向有功电能", "unit": "Kwh", "max_id": 0}]},
        {"主路电表, 当前反向有功电能": [{"name": "当前反向有功电能", "unit": "Kwh", "max_id": 0}]},
        {"主路电表, 电压": [{"name": "电压", "unit": "V", "max_id": 0}]},
        {"主路电表, 电流": [{"name": "电流", "unit": "A", "max_id": 0}]},
        {"主路电表, 功率": [{"name": "功率", "unit": "Kw", "max_id": 0}]},
        {"主路电表, 功率因数": [{"name": "功率因数", "unit": "-", "max_id": 0}]},
        {"主路电表, 频率": [{"name": "频率", "unit": "Hz", "max_id": 0}]},
        {"主路电表, 设备通讯状态": [{"name": "设备通讯状态", "unit": "-", "0": "通讯中断", "1": "通讯正常", "max_id": 0}]}]},

    {"空调": [
        {"空调, 吸气温度探头故障": [{"name": "吸气温度探头故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 送风温度探头故障": [{"name": "送风温度探头故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 吸气压力探头故障": [{"name": "吸气压力探头故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 排气压力探头故障": [{"name": "排气压力探头故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 回风温度探头故障": [{"name": "回风温度探头故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 回风湿度探头故障": [{"name": "回风湿度探头故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 温度过高": [{"name": "温度过高", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 送风温度过低": [{"name": "送风温度过低", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 湿度过高": [{"name": "湿度过高", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 湿度过低": [{"name": "湿度过低", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 水溢报警": [{"name": "水溢报警", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 漏水报警": [{"name": "漏水报警", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 高压保护开关": [{"name": "高压保护开关", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 低压保护开关": [{"name": "低压保护开关", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 烟雾报警": [{"name": "烟雾报警", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 送风机故障": [{"name": "送风机故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 加湿器故障": [{"name": "加湿器故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 电加热故障": [{"name": "电加热故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 水泵故障": [{"name": "水泵故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 低压压力报警": [{"name": "低压压力报警", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 电流过载": [{"name": "电流过载", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 排气压力过高报警": [{"name": "排气压力过高报警", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 压缩机内部故障": [{"name": "压缩机内部故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 压缩机通讯故障": [{"name": "压缩机通讯故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 送风机": [{"name": "送风机", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 压缩机": [{"name": "压缩机", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 冷凝水泵": [{"name": "冷凝水泵", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 低温电磁阀": [{"name": "低温电磁阀", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 故障": [{"name": "故障", "unit": "-", "0": "正常", "1": "故障", "max_id": 0}]},
        {"空调, 远控": [{"name": "远控", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 开关机": [{"name": "开关机", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 温度设定": [{"name": "温度设定", "unit": "℃", "max_id": 0}]},
        {"空调, 湿度设置": [{"name": "湿度设置", "unit": "%", "max_id": 0}]},
        {"空调, 来电自启动": [{"name": "来电自启动", "unit": "-", "0": "禁用", "1": "启用", "max_id": 0}]},
        {"空调, 温度回差": [{"name": "温度回差", "unit": "℃", "max_id": 0}]},
        {"空调, 湿度回差": [{"name": "湿度回差", "unit": "%", "max_id": 0}]},
        {"空调, 除湿使能": [{"name": "除湿使能", "unit": "-", "0": "禁用", "1": "启用", "max_id": 0}]},
        {"空调, 联网地址设置": [{"name": "联网地址设置", "unit": "-", "max_id": 0}]},
        {"空调, 压缩机电流过载": [{"name": "压缩机电流过载", "unit": "A", "max_id": 0}]},
        {"空调, 控制方式": [{"name": "控制方式", "unit": "-", "0": "回风", "1": "送风", "max_id": 0}]},
        {"空调, 吸气压力量程": [{"name": "吸气压力量程", "unit": "Bar", "max_id": 0}]},
        {"空调, 最低送风温度": [{"name": "最低送风温度", "unit": "℃", "max_id": 0}]},
        {"空调, 最高送风温度": [{"name": "最高送风温度", "unit": "℃", "max_id": 0}]},
        {"空调, 高温报警": [{"name": "高温报警", "unit": "℃", "max_id": 0}]},
        {"空调, 送风低温报警": [{"name": "送风低温报警", "unit": "℃", "max_id": 0}]},
        {"空调, 高湿报警": [{"name": "高湿报警", "unit": "%", "max_id": 0}]},
        {"空调, 低湿报警": [{"name": "低湿报警", "unit": "%", "max_id": 0}]},
        {"空调, 吸气压力报警": [{"name": "吸气压力报警", "unit": "Bar", "max_id": 0}]},
        {"空调, 排气压力量程": [{"name": "排气压力量程", "unit": "Bar", "max_id": 0}]},
        {"空调, 排压压力报警": [{"name": "排压压力报警", "unit": "Bar", "max_id": 0}]},
        {"空调, 送风机输出": [{"name": "送风机输出", "unit": "%", "max_id": 0}]},
        {"空调, 机组运行时间": [{"name": "机组运行时间", "unit": "-", "max_id": 0}]},
        {"空调, 压机运行时间": [{"name": "压机运行时间", "unit": "-", "max_id": 0}]},
        {"空调, 过热度": [{"name": "过热度", "unit": "℃", "max_id": 0}]},
        {"空调, EEV开度": [{"name": "EEV开度", "unit": "%", "max_id": 0}]},
        {"空调, 吸气温度": [{"name": "吸气温度", "unit": "℃", "max_id": 0}]},
        {"空调, 送风温度": [{"name": "送风温度", "unit": "℃", "max_id": 0}]},
        {"空调, 吸气压力": [{"name": "吸气压力", "unit": "Bar", "max_id": 0}]},
        {"空调, 排气压力": [{"name": "排气压力", "unit": "Bar", "max_id": 0}]},
        {"空调, 室内温度": [{"name": "室内温度", "unit": "℃", "max_id": 0}]},
        {"空调, 室内湿度": [{"name": "室内湿度", "unit": "%", "max_id": 0}]},
        {"空调, 压缩机频率": [{"name": "压缩机频率", "unit": "Hz", "max_id": 0}]},
        {"空调, 蒸发温度": [{"name": "蒸发温度", "unit": "℃", "max_id": 0}]},
        {"空调, 滤网维护故障": [{"name": "滤网维护故障", "unit": "-", "0": "故障", "1": "正常", "max_id": 0}]},
        {"空调, 制热开偏差": [{"name": "制热开偏差", "unit": "℃", "max_id": 0}]},
        {"空调, 制热关偏差": [{"name": "制热关偏差", "unit": "℃", "max_id": 0}]},
        {"空调, 加湿使能": [{"name": "加湿使能", "unit": "-", "0": "禁止", "1": "使能", "max_id": 0}]},
        {"空调, 加热使能": [{"name": "加热使能", "unit": "-", "0": "禁止", "1": "使能", "max_id": 0}]},
        {"空调, 变频器工作状态": [{"name": "变频器工作状态", "unit": "-", "0": "通讯中断", "1": "通讯正常", "max_id": 0}]},
        {"空调, 电加热": [{"name": "电加热", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 加湿器": [{"name": "加湿器", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 旁通电磁阀": [{"name": "旁通电磁阀", "unit": "-", "0": "关闭", "1": "开启", "max_id": 0}]},
        {"空调, 液管温度": [{"name": "液管温度", "unit": "℃", "max_id": 0}]},
        {"空调, 设备通讯状态": [{"name": "设备通讯状态", "unit": "-", "0": "通讯中断", "1": "通讯正常", "max_id": 0}]}]}
]


# 告警实时数据
@accept_websocket
def echo(request):
    if not request.is_websocket():  # 如果不是socket链接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            print("普通的http方法")
            return HttpResponse(message)
        except:
            print("普通的http方法报错")
            return HttpResponse("普通的http方法报错")
    else:
        for message in request.websocket:
            # print(request.websocket)
            # print(message)
            # websockt传递的是二进制数据
            print("前端传过来的数据：%s" % message.decode())
            # 通过DataConfigTool收集 这些标准信息
            while True:
                list_data = []  # 严重告警列表
                list_data1 = []  # 一般告警列表
                # 获取模块的字典对象[{"监控屏IO":[{},{},{},...]},...,...]
                for item in list_war:
                    # 获取模块名称"equipment=监控屏IO"，及模块里面的设备列表value = [{"监控屏IO, 烟感": ["烟雾告警", "有告警", "严重告警", "-", 1]},{...},{...},...]
                    for equipment, value in item.items():
                        # 获得字典对象
                        # print(equipment)
                        for value_list in value:
                            # 获得告警设备和告警信息
                            for eq_name, alarm in value_list.items():
                                # print(alarm)
                                # ---------------------《 严重告警存入数据库 》----------------------
                                if alarm[2] == "严重告警" and eq_name == "温湿度, 温度":
                                    data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                    # 获取最新的ID 将其保存到全局变量“max1_id”，然后来做第二次对比判断
                                    # 防止将重复的数据存入告警表中，拿id做比对
                                    if alarm[5]["max_id"] != data.id:
                                        alarm[5]["max_id"] = data.id
                                        # 将告警存入数据库
                                        Warning.objects.create(
                                            warn_level=alarm[2],
                                            warn_text=alarm[0],
                                            warn_time=data.data_time,
                                            warn_name=equipment,
                                            warn_data=data.float_data,
                                            unit=alarm[3],
                                            is_delete=False,
                                            warn_ip=data.divice_ip,
                                            # 查询到对应站点（通过ip）
                                            equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                        )
                                    if alarm[5]["max_id"] == data.id:
                                        pass
                                    if data.float_data >= alarm[4]:
                                    # if data.float_data >= 20:
                                        # 告警站点
                                        divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                            values("divice_name")[0]["divice_name"]
                                        # 告警设备
                                        alarm_model = equipment
                                        # 告警名称
                                        alarm_divice = alarm[0]
                                        # 告警内容
                                        # print(type(data.float_data))
                                        # print(type(alarm[3]))
                                        alarm_data = str(data.float_data) + alarm[3]
                                        # 告警时间
                                        alarm_time = data.data_time
                                        # 告警等级
                                        alarm_level = alarm[2]
                                        # 传给前端的数据
                                        data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                     "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                     "alarm_time": alarm_time, "alarm_level": alarm_level}
                                        # 将每一条数据添加到列表
                                        list_data.append(data_dict)
                                # 判断
                                if alarm[2] == "严重告警" and eq_name != "温湿度, 温度":
                                    data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                    # 获取最新的ID 将其保存到全局变量“max1_id”，然后来做第二次对比判断
                                    if alarm[5]["max_id"] != data.id:
                                        alarm[5]["max_id"] = data.id
                                        Warning.objects.create(
                                            warn_level=alarm[2],
                                            warn_text=alarm[0],
                                            warn_time=data.data_time,
                                            warn_name=equipment,
                                            warn_data=data.float_data,
                                            unit=alarm[3],
                                            is_delete=False,
                                            warn_ip=data.divice_ip,
                                            # 查询到对应站点（通过ip）
                                            equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                        )
                                    if alarm[5]["max_id"] == data.id:
                                        pass
                                    if data.float_data != alarm[4]:
                                    # if data.float_data == alarm[4]:
                                        # 告警站点
                                        divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                            values("divice_name")[0]["divice_name"]
                                        # 告警设备
                                        alarm_model = equipment
                                        # 告警名称
                                        alarm_divice = alarm[0]
                                        # 告警内容
                                        alarm_data = alarm[1]
                                        # 告警时间
                                        alarm_time = data.data_time
                                        # 告警等级
                                        alarm_level = alarm[2]
                                        # 传给前端的数据
                                        data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                     "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                     "alarm_time": alarm_time, "alarm_level": alarm_level}
                                        # 将每一条数据添加到列表
                                        list_data.append(data_dict)

                                # ---------------------《一般告警存入数据库 》----------------------
                                if alarm[2] != "严重告警":
                                    if eq_name == "温湿度, 温度" and alarm[0] == "低温告警":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        # 获取最新的ID 将其保存到全局变量“max1_id”，然后来做第二次对比判断
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5]["max_id"] == data.id:
                                            pass
                                        if data.float_data <= alarm[4]:
                                        # if data.float_data <= 30:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = str(data.float_data) + alarm[3]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                                    if eq_name == "温湿度, 湿度" and alarm[0] == "高湿告警":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5].get("max_id") == data.id:
                                            pass
                                        if data.float_data >= alarm[4]:
                                        # if data.float_data >= 30:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = str(data.float_data) + alarm[3]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                                    if eq_name == "温湿度, 湿度" and alarm[0] == "低湿告警":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5].get("max_id") == data.id:
                                            pass
                                        if data.float_data <= alarm[4]:
                                        # if data.float_data <= 30:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = str(data.float_data) + alarm[3]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                                    if eq_name != "温湿度, 温度":
                                        data = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                                        if alarm[5]["max_id"] != data.id:
                                            alarm[5]["max_id"] = data.id
                                            Warning.objects.create(
                                                warn_level=alarm[2],
                                                warn_text=alarm[0],
                                                warn_time=data.data_time,
                                                warn_name=equipment,
                                                warn_data=data.float_data,
                                                unit=alarm[3],
                                                is_delete=False,
                                                warn_ip=data.divice_ip,
                                                # 查询到对应站点（通过ip）
                                                equip_id=divices.objects.get(divice_ip=data.divice_ip)
                                            )
                                        if alarm[5].get("max_id") == data.id:
                                            pass
                                        if data.float_data != alarm[4]:
                                        # if data.float_data == alarm[4]:
                                            # 告警站点
                                            divice_id = divices.objects.filter(divice_ip=data.divice_ip). \
                                                values("divice_name")[0]["divice_name"]
                                            # 告警设备
                                            alarm_model = equipment
                                            # 告警名称
                                            alarm_divice = alarm[0]
                                            # 告警内容
                                            alarm_data = alarm[1]
                                            # 告警时间
                                            alarm_time = data.data_time
                                            # 告警等级
                                            alarm_level = alarm[2]
                                            # 传给前端的数据
                                            data_dict = {"divice_id": divice_id, "alarm_model": alarm_model,
                                                         "alarm_divice": alarm_divice, "alarm_data": alarm_data,
                                                         "alarm_time": alarm_time, "alarm_level": alarm_level}
                                            # 将每一条数据添加到列表
                                            list_data1.append(data_dict)
                # ----------------------------------<存入历史数据>--------------------------------------
                store_historyData()
                # ----------------------------------<详情页面 实时更新数据 环境实时数据数据>--------------------------------------
                data_dict = {
                    # 环境
                    "AC_SAT": XmlData.objects.filter(name="空调, 送风温度").order_by("-id").first().float_data,
                    "AC_RAT": XmlData.objects.filter(name="空调, 吸气温度").order_by("-id").first().float_data,
                    "AC_RAH": XmlData.objects.filter(name="空调, 室内湿度").order_by("-id").first().float_data,
                    "AC_ST": "开" if int(
                        XmlData.objects.filter(name="空调, 设备通讯状态").order_by("-id").first().float_data) == 1 else "关",
                    # 电力
                    "PW_MV": XmlData.objects.filter(name="UPS, 输入电压").order_by("-id").first().float_data,
                    "PW_OV": XmlData.objects.filter(name="UPS, 输出电压").order_by("-id").first().float_data,
                    "PW_LR": XmlData.objects.filter(name="UPS, 输出负载率").order_by("-id").first().float_data,
                    "PW_BT": XmlData.objects.filter(name="UPS, 电池剩余时间").order_by("-id").first().float_data,
                    "PW_ROW": XmlData.objects.filter(name="主路电表, 功率").order_by("-id").first().float_data,
                    "PW_EC": XmlData.objects.filter(name="UPS, 输出功率因素").order_by("-id").first().float_data,
                    # 安防
                    "DR_ST": "开" if int(
                        XmlData.objects.filter(name="监控屏IO, 机柜门").order_by("-id").first().float_data) == 1 else "关",
                    # "DR_VD": XmlData.objects.filter(name="UPS, 输出功率因素").order_by("-id").first().float_data,
                    # 其他
                    "DR_MW": "无" if int(
                        XmlData.objects.filter(name="监控屏IO, 漏水").order_by("-id").first().float_data) == 1 else "有",
                    "DR_SD": "无" if int(
                        XmlData.objects.filter(name="监控屏IO, 烟感").order_by("-id").first().float_data) == 1 else "有",

                }
                # 将“严重告警”和“一般告警”发送前端
                data_dict = {"严重告警": list_data, "一般告警": list_data1, "data_dict": data_dict}
                # 转换成json格式传送
                str_list = json.dumps(data_dict)
                # print("返回给前端的数据", str_list)
                # 发送消息到客户端
                request.websocket.send(str_list.encode())
                list_data.clear()
                list_data1.clear()


# 用于展示历史数据(结合list_eq查询xmldata)
def store_historyData():
    for item in list_eq:
        # 获取模块名称"equipment=监控屏IO"，及模块里面的设备列表value = [{...},{...},{...},...]
        for equipment, value in item.items():
            # 获得字典对象
            # print(equipment)
            for value_list in value:
                # 获得告警设备和告警信息
                for eq_name, alarm in value_list.items():
                    # print(eq_name)
                    # print(alarm)
                    xmldata_obj = XmlData.objects.filter(name=eq_name).order_by("-id").first()
                    # print(xmldata_obj[0])
                    # print(xmldata_obj.id)
                    if alarm[0]["max_id"] != xmldata_obj.id:
                        alarm[0]["max_id"] = xmldata_obj.id
                        # print(alarm[0]["max_id"])
                        # 先得到所有的key 然后判断float_data==key
                        key_list = list(alarm[0].keys())
                        # print(key_list)
                        # 遍历key_list 与取得的浮点数（转化后）相等，通过key取得对应的value
                        value_data = [alarm[0][key] for key in key_list if str(int(xmldata_obj.float_data)) == key]
                        # 判断value_data 为空则赋值null
                        value_data_lsit = value_data[0] if value_data != [] else str(xmldata_obj.float_data)
                        # print(value_data_lsit)
                        EquipmentData.objects.create(
                            # 设备
                            equipment=equipment,
                            # 设备名称
                            equipment_name=alarm[0]["name"],
                            # 信息值
                            equipment_folat=xmldata_obj.float_data,
                            # 内容根据信息值判断
                            equipment_text=value_data_lsit,
                            # 单位
                            equipment_unit=alarm[0]["unit"],
                            # 时间
                            equipment_time=xmldata_obj.data_time,
                            # 关联IP
                            equipment_ip=xmldata_obj.divice_ip,
                            # 外建
                            divices=divices.objects.get(divice_ip=xmldata_obj.divice_ip)

                        )
                    if alarm[0]["max_id"] == xmldata_obj.id:
                        pass
