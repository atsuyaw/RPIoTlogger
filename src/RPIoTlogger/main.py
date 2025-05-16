APP = 'RPIoTlogger'
VER = '0.2.0'
#
from config import *
from intTemp import *
from OneTemp import *
from postAPI import *
from rawADC import *

# SSID =
# PASSWORD =
# HOSTNAME =
# REMOTE =
# ORG_ID =
# BUCKET =
# ACCESS_TOKEN =
from machine import Pin
from hx711 import *
import time
from wifi import *

print("IP: " + connect())
MAC = getMac()

hx = hx711(Pin(14), Pin(15))
hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_10)

while True:
    INT_TEMP = aveIntTemp()
    ADC_CUR_PIN = 1
    COEFF_CUR = 6.7625
    SHIFT_CUR = 0.0118
    CUR = aveRawV(ADC_CUR_PIN,COEFF_CUR,SHIFT_CUR)
    ADC_VOL_PIN = 0
    COEFF_VOL = 81.331
    SHIFT_VOL = 0.1398
    VOL = aveRawV(ADC_VOL_PIN,COEFF_E,SHIFT_E)
    ONE_TEMP_PIN = 12
    ONE_TEMP = aveOneTemp(ONE_TEMP_PIN)
    WEIGHT = hx.get_value()
    DATUM = f'int_temp={INT_TEMP},'\
            + f'one_temp={ONE_TEMP},'\
            + f'current={CUR}'\
            + f'voltage={VOL},'\
            + f'weight={WEIGHT},'\
            + f'app={APP},'\
            + f'ver={VER}'
    postAPI(MAC, DATUM)
    utime.sleep(30)
