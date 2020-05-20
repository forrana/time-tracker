import machine
import time
from imu import MPU6050
import deltat
from fusion import Fusion
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(19))
i2c.scan()
imu = MPU6050(i2c)
fuse = Fusion()
print(imu.accel.xyz)

while(True):
    time.sleep_ms(500)
    print(imu.accel.xyz)

while True:
    fuse.update_nomag(imu.accel.xyz, imu.gyro.xyz) # Note blocking mag read
    if count % 50 == 0:
        print("Heading, Pitch, Roll: {:7.3f} {:7.3f} {:7.3f}".format(fuse.heading, fuse.pitch, fuse.roll))
    time.sleep_ms(20)
    count += 1

from machine import TouchPad, Pin
t = TouchPad(Pin(4))
t.config(500)
t.read()

def touch():
    if t.read() < 300:
        return True
    else:
        return False
