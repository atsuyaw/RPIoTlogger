import machine
import utime

def getRawV(PIN,COEFF,SHIFT):
    VIN = machine.ADC(PIN)
    CONV = 1 / 65535
    result = []
    for i in range(100):
        RAWV = VIN.read_u16() * CONV * COEFF + SHIFT
        # print(RAWV)
        utime.sleep_ms(10)
        result.append(RAWV)
    return result


def aveRawV(PIN,COEFF,SHIFT):
    try:
        list = getRawV(PIN,COEFF,SHIFT)
        avg = sum(list) / len(list)
        return avg
    except IndexError:
        return 0
