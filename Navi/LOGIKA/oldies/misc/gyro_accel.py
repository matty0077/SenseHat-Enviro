#!/usr/bin/python

import sys, getopt
sys.path.append("/home/pi/Desktop/NAVI/WANDER_LUST")
sys.path.append('.')
import RTIMU
import os.path
import time
import math
from sense_hat import SenseHat
sense=SenseHat()
sense.set_rotation(180)
# Note: timestamp is in microseconds
#sense.load_image("/home/pi/Desktop/NAVI/WANDER_LUST/memory/media/GYRO/gyrot.png")
timestamp = 0

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
imu.IMUInit()

print("IMU Name: " + imu.IMUName())

# set some gyro rate here to test (units: rads/s)

gx = 0.0
gy = 0.0
gz = 0.1

# set accel to indicate horizontal (units: g)

ax = 0.0
ay = 0.0
az = 1.0

# set mag to whatever (or leave as 0 if turned off) (units: uT)

mx = 0.0
my = 0.0
mz = 0.0

# this is how to turn off the magnetometer

imu.setCompassEnable(False)

# everything is now ready
#i=['gyro.png','gyro1.png','gyro2.png']
#sense.load_image("/home/pi/Desktop/NAVI/WANDER_LUST/memory/media/GYRO/"+i)

while True:
  raw=sense.get_gyroscope_raw()
  #print(sense.gyro_raw)
  GG='y:{y}'.format(**raw)
  #print(GG)
  try:

    #print("gz: %f" % gz)
    #imu.setExtIMUData(gx, gy, gz, ax, ay, az, mx, my, mz, timestamp)
    #data = imu.getIMUData()
    #fusionPose = data["fusionPose"]
    #print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), 
        #math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
    time.sleep(0.1)
    timestamp += 100000
    if GG>0:
      print(GG)
      sense.load_image("/home/pi/Desktop/NAVI/WANDER_LUST/memory/media/GYRO/gyro1.png")
    elif GG<0:
      print(GG)
      sense.load_image("/home/pi/Desktop/NAVI/WANDER_LUST/memory/media/GYRO/gyro2.png")
    else:
      print(GG)
      sense.load_image("/home/pi/Desktop/NAVI/WANDER_LUST/memory/media/GYRO/gyro0.png")
  except KeyboardInterrupt:
      import Saving_Grace
      sys.exit()
