# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, pyb
from pyb import LED
from pyb import UART
from pyb import I2C

class BCD:
    def bcdDigits(self, chars):
        for char in chars:
#            char = ord(char)
            for val in (char >> 4, char & 0xF):
                if val==0xF:
                    return
                return val



try:
    uart = UART(1)
    uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)
    print(uart)
except ValueError:
    print("error: baud rate +- 5% out of range")

#i2c=I2C(2, I2C.MASTER)
#i2c.init(I2C.MASTER, baudrate=100000)

#Setting RTC regs to actual time
#i2c.mem_write(0x00,0x68,0, timeout=1000)
#i2c.mem_write(0x04,0x68,1, timeout=1000)
#i2c.mem_write(0x15,0x68,2, timeout=1000)
#i2c.mem_write(0x03,0x68,3, timeout=1000)
#i2c.mem_write(0x17,0x68,4, timeout=1000)
#i2c.mem_write(0x05,0x68,5, timeout=1000)
#i2c.mem_write(0x19,0x68,6, timeout=1000)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
ir_leds = pyb.LED(4)
ir_leds.on()
#print(i2c.is_ready(0x68))
#test=BCD()
#p=pyb.Pin("P3", pyb.Pin.OUT_PP)
p=pyb.Pin("P3", pyb.Pin.IN, pyb.Pin.PULL_DOWN)


while(True):
#    uart.write("RAT\r")
#    pyb.delay(1000)
#    print(uart.read(60))
#    pyb.delay(1000)
#    pyb.delay(5000)
#    x=(i2c.mem_read(1, 0x68, 0))
#    z=ord(x) & 0xF
#    y=test.bcdDigits(x)
#    print(y,z)
#    x=(i2c.mem_read(1, 0x68, 1))
#    z=ord(x) & 0xF
#    y=test.bcdDigits(x)
#    print(y,z)
#    x=(i2c.mem_read(1, 0x68, 2))
#    z=ord(x) & 0xF
#    y=test.bcdDigits(x)
#    print(y,z)
#    x=(i2c.mem_read(1, 0x68, 3))
#    z=ord(x) & 0xF
#    y=test.bcdDigits(x)
#    print(y,z)
#    x=(i2c.mem_read(1, 0x68, 4))
#    z=ord(x) & 0xF
#    y=test.bcdDigits(x)
#    print(y,z)
#    x=(i2c.mem_read(1, 0x68, 5))
#    z=ord(x) & 0xF
#    y=test.bcdDigits(x)
#    print(y,z)
#    x=(i2c.mem_read(1, 0x68, 6))
#    z=ord(x) & 0xF
#    y=test.bcdDigits(x)
#    print(y,z)
#    p.high()
#    pyb.delay(5000)
#    p.low()
    print(p.value())
    pyb.delay(1000)

