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
SETTINGS_FILE = "RTIMULib"
    
#  computeHeight() - the conversion uses the formula:
#
#  h = (T0 / L0) * ((p / P0)**(-(R* * L0) / (g0 * M)) - 1)
#
#  where:
#  h  = height above sea level
#  T0 = standard temperature at sea level = 288.15
#  L0 = standard temperatur elapse rate = -0.0065
#  p  = measured pressure
#  P0 = static pressure = 1013.25
#  g0 = gravitational acceleration = 9.80665
#  M  = mloecular mass of earth's air = 0.0289644
#  R* = universal gas constant = 8.31432
#
#  Given the constants, this works out to:
#
#  h = 44330.8 * (1 - (p / P0)**0.190263)

class Atmos:
    def message(self,message):
        #///////////rotate display
        x=round(sense.get_accelerometer_raw()['x'],0)
        y=round(sense.get_accelerometer_raw()['y'],0)
        #while True:
        if x==-1:
            sense.set_rotation(90)
        elif y==-1:
            sense.set_rotation(180)
        elif x==1:
            sense.set_rotation(270)
        sense.show_message(message,scroll_speed=.04)#text_colour=red)backcolor

    def computeHeight(self,pressure):
        return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));
    
    def run(self):
        print("Using settings file " + SETTINGS_FILE + ".ini")
        if not os.path.exists(SETTINGS_FILE + ".ini"):
          print("Settings file does not exist, will be created")

        s = RTIMU.Settings(SETTINGS_FILE)
        imu = RTIMU.RTIMU(s)
        pressure = RTIMU.RTPressure(s)

        print("IMU Name: " + imu.IMUName())
        print("Pressure Name: " + pressure.pressureName())

        if (not imu.IMUInit()):
            print("IMU Init Failed")
            sys.exit(1)
        else:
            print("IMU Init Succeeded");

        # this is a good time to set any fusion parameters

        imu.setSlerpPower(0.02)
        imu.setGyroEnable(True)
        imu.setAccelEnable(True)
        imu.setCompassEnable(True)

        if (not pressure.pressureInit()):
            print("Pressure sensor Init Failed")
        else:
            print("Pressure sensor Init Succeeded")

        poll_interval = imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % poll_interval)
        while True:
            try:
              if imu.IMURead():
                # x, y, z = imu.getFusionData()
                # print("%f %f %f" % (x,y,z))
                data = imu.getIMUData()
                (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
                fusionPose = data["fusionPose"]
                self.message("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), 
                    math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
                if (data["pressureValid"]):
                    self.message("Pressure: %f, height above sea level: %f" % (data["pressure"], self.computeHeight(data["pressure"])))
                if (data["temperatureValid"]):
                    self.message("Temperature: %f" % (data["temperature"]))
                time.sleep(poll_interval*1.0/1000.0)
            except KeyboardInterrupt:
                import Saving_Grace
                sys.exit()

T=Atmos()
T.run()
