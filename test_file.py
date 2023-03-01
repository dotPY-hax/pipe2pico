import time
import machine
import sys

led = machine.Pin("LED", machine.Pin.OUT)
led.toggle()
time.sleep(1)
led.toggle()
sys.implementation