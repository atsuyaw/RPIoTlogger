# https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
# https://teratail.com/questions/buag9os7aoj9en
import machine
import utime

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

def get_sensor_temp():
    result = []
    for i in range(10):
        reading = sensor_temp.read_u16() * conversion_factor
        sensorTemp = 27 - (reading - 0.706)/0.001721
        print(sensorTemp)
        utime.sleep_ms(10)
        result.append(sensorTemp)
    return result


def aveIntTemp():
    list = get_sensor_temp()
    print(list)
    avg = sum(list) / len(list)
    # print("avg: " + str(avg))
    return avg

