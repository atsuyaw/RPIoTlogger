import machine
import time
LED = machine.Pin("LED", machine.Pin.OUT)


def blink(SIG, DUR):
    for i in range(SIG):
        LED.value(0)#  Turn off now
        time.sleep(DUR)#  Wait 0.5s
        LED.value(1)
        time.sleep(DUR)
        LED.value(0)
