from hx711 import *
from intTemp import *
from machine import Pin
from OneTemp import *
from postAPI import *
from secrets import *
from rawADC import *
from wifi import *
from version import *

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
    CUR = aveRawV(ADC_CUR_PIN, COEFF_CUR, SHIFT_CUR)
    ADC_VOL_PIN = 0
    COEFF_VOL = 81.331
    SHIFT_VOL = 0.1398
    VOL = aveRawV(ADC_VOL_PIN, COEFF_VOL, SHIFT_VOL)
    ONE_TEMP_PIN = 12
    ONE_TEMP = aveOneTemp(ONE_TEMP_PIN)
    WEIGHT = hx.get_value()
    DATUM = (
        f"int_temp={INT_TEMP},"
        + f"one_temp={ONE_TEMP},"
        + f"current={CUR},"
        + f"voltage={VOL},"
        + f"weight={WEIGHT},"
        + f'app="{__app__}",'
        + f'ver="{__version__}"'
    )
    postAPI(MAC, DATUM)
    utime.sleep(30)
