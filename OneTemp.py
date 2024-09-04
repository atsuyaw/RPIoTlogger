#!/usr/bin/env python
# -*- coding: utf-8 -*
from machine import Pin
import onewire
import ds18x20
import time
# https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
# https://teratail.com/questions/buag9os7aoj9en
import machine
import utime

def getOneTemp(PIN):
    ow = onewire.OneWire(Pin(PIN))# 1-Wire path
    ds = ds18x20.DS18X20(ow)# ds18x20 class instance
    ## get rom code
    roms = ds.scan()        # 64bit roms <class 'list'>
    print('roms=',roms)
    rom=roms[0]# Set [0] because there is only DS18B20 for 1-Wire
    result = []
    for i in range(10):
        temp = ds.convert_temp()       # 温度データをSCRATCHPADに保存
        time.sleep_ms(750)      # 分解能12bitの場合
        temp=ds.read_temp(rom)  #　摂氏温度で取得
        print(temp)
        utime.sleep_ms(10)
        result.append(temp)
    return result
def aveOneTemp(PIN):
    list = getOneTemp(PIN)
    print(list)
    avg = sum(list) / len(list)
    # print("avg: " + str(avg))
    return avg
