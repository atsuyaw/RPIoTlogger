import machine
import utime


def getRawV(PIN, VMAX):
    VIN = machine.ADC(PIN)
    conversion_factor = VMAX / 65535
    result = []
    for i in range(10):
        RAWV = VIN.read_u16() * conversion_factor
        # print(RAWV)
        utime.sleep_ms(10)
        result.append(RAWV)
    return result


def aveRawV(PIN, VMAX):
    list = getRawV(PIN, VMAX)
    # print(list)
    avg = sum(list) / len(list)
    # print(avg)
    return avg
