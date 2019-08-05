#!/usr/bin/python
import sys
sys.path.append("/home/pi/Desktop/NAVI/SPIRIT/WANDER_LUST/")
sys.path.append("/home/pi/Desktop/NAVI/SPIRIT/WANDER_LUST/memory/Navi/LOGIKA/")
from sense_hat import SenseHat
from datetime import datetime
import os
from evdev import InputDevice, ecodes, list_devices
from select import select
import logging
import time
import subprocess

found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True;
        break

if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()
# 0, 0 = Top left
# 7, 7 = Bottom right
UP_PIXELS = [[3, 0], [4, 0]]
DOWN_PIXELS = [[3, 7], [4, 7]]
LEFT_PIXELS = [[0, 3], [0, 4]]
RIGHT_PIXELS = [[7, 3], [7, 4]]
CENTRE_PIXELS = [[3, 3], [4, 3], [3, 4], [4, 4]]
blue=(0,0,255)
yellow=(255,255,0)
red = (255, 0, 0)
white=(255,255,255)
black=(0,0,0)
green = (0, 255, 0)

#balancer
r = (255,0,0)
b = (0,0,0)
w = (255,255,255)
g = (0,255,0)

x = 1
y = 1

game_over = False

maze = [
[r,r,r,r,r,r,r,r],
[r,b,b,b,b,b,b,r],
[r,b,b,b,b,b,b,r],
[r,b,b,b,b,b,b,r],
[r,b,b,b,b,b,b,r],
[r,b,b,b,b,b,b,r],
[r,b,b,b,b,b,b,r],
[r,r,r,r,r,r,r,r]]
#lvler
r = [255, 0, 0]
g = [0, 255, 0]
b = [0, 0, 255]
w = [255,255,255]
z = [0, 0, 0]

redimage = [
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
]

greenimage = [
w,w,w,w,w,w,w,w,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
]

blueimage = [
w,w,w,w,w,w,w,w,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
]

whiteimage = [
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,z,z,w,w,w,
w,w,w,z,z,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
]
#compass
# To get good results with the magnetometer you must first calibrate it using
# the program in RTIMULib/Linux/RTIMULibCal
# The calibration program will produce the file RTIMULib.ini
# Copy it into the same folder as your Python code
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
import getopt
sys.path.append('.')
import RTIMU
import os.path
import math
import gps3
import threading
sense = SenseHat()
sense.clear()

class Master:
    run=True
#//////////////messenger
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

#/#//////////////////////threader
    def Threader(self,action):
        THREAD=threading.Thread(target=action)
        #THREAD.daemon=True
        THREAD.start()
        #THREAD.join()#join---optional?
#////////////////emoji animator
    def anime(self,folder):
        i=0
        listo=[]
        path=(folder)
        for file in os.listdir(path):
            if file.endswith(".png"):
                i+=1
                listo.append(file)#add directory files to list
        for i in listo:
            sense.load_image(folder+i)
            #print(i)
            time.sleep(.1)
#////////////////////////////gentle close from freefaller

    def gentle_close(self): # A function to end the program gracefully
        #self.run=False
        sense.clear(255,0,0) # Turn on the LEDs red
        time.sleep(0.25) # Wait half a second
        sense.clear(0,0,0) # Turn all the LEDs off
        p=subprocess.Popen(['sudo','/home/pi/Desktop/NAVI/SPIRIT/WANDER_LUST/memory/Navi/Master.py'],shell=False)
        p.terminate()
        #p.kill()
        p.wait()
        #import Saving_Grace
        
#////////////////////////////////compass

    def compass(self):
        sense.clear()
        sense.set_rotation(90)
        led_loop = [4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8, 0, 1, 2, 3]

        prev_x = 0
        prev_y = 0

        led_degree_ratio = len(led_loop) / 360.0
        self.Threader(G.Manual)
        while self.run==True:
            try:
                dir = sense.get_compass()
                dir_inverted = 360 - dir  # So LED appears to follow North
                led_index = int(led_degree_ratio * dir_inverted)
                offset = led_loop[led_index]

                y = offset // 8  # row
                x = offset % 8  # column

                if x != prev_x or y != prev_y:
                    sense.set_pixel(prev_x, prev_y, 0, 0, 0)

                sense.set_pixel(x, y, 0, 0, 255)

                prev_x = x
                prev_y = y
            except KeyboardInterrupt:
                sense.clear()
                self.gentle_close()
                break
        else:
            self.gentle_close()
#/////////////////////////////seeker
            
    def HeatFinder(self):
        #sense.set_rotation(90)
        sense.clear()
        self.Threader(self.Manual)
        while self.run==True:
            try:
                temp = sense.temp
                #print(temp)
                pixels = [red if i < temp else blue for i in range(64)]
                sense.set_pixels(pixels)
                time.sleep(.1)    
                    
            except KeyboardInterrupt:
                sense.clear()
                self.gentle_close()
                break     
        else:
            self.gentle_close()
            
    def HumidFinder(self):
        #sense.set_rotation(90)
        sense.clear()
        self.Threader(self.Manual)
        while self.run==True:
            try:
                humidity = sense.humidity
                humidity_value = 64 * humidity / 100
                print(humidity)
                pixels = [green if i < humidity_value else white for i in range(64)]
                sense.set_pixels(pixels)
            except KeyboardInterrupt:
                sense.clear()
                self.gentle_close()
                break
        else:
            self.gentle_close()
#////////////////////////////////////temp humid
    def atmos(self):
        self.Threader(self.Manual)

        def computeHeight(pressure):
            return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));
        
        #def run():
        print("Using settings file " + SETTINGS_FILE + ".ini")
        if not os.path.exists(SETTINGS_FILE + ".ini"):
          print("Settings file does not exist, will be created")

        s = RTIMU.Settings(SETTINGS_FILE)
        imu = RTIMU.RTIMU(s)
        pressure = RTIMU.RTPressure(s)
        humidity = RTIMU.RTHumidity(s)

        print("IMU Name: " + imu.IMUName())
        print("Pressure Name: " + pressure.pressureName())
        print("Humidity Name: " + humidity.humidityName())

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

        if (not humidity.humidityInit()):
            print("Humidity sensor Init Failed")
        else:
            print("Humidity sensor Init Succeeded")

        poll_interval = imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % poll_interval)

        while self.run==True:
            try:
              if imu.IMURead():
                # x, y, z = imu.getFusionData()
                # print("%f %f %f" % (x,y,z))
                data = imu.getIMUData()
                (data["pressureValid"], data["pressure"], data["pressureTemperatureValid"], data["pressureTemperature"]) = pressure.pressureRead()
                (data["humidityValid"], data["humidity"], data["humidityTemperatureValid"], data["humidityTemperature"]) = humidity.humidityRead()
                fusionPose = data["fusionPose"]
                self.message("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), 
                    math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
                if (data["pressureValid"]):
                    self.message("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["pressure"])))
                if (data["pressureTemperatureValid"]):
                    self.message("Pressure temperature: %f" % (data["pressureTemperature"]))
                if (data["humidityValid"]):
                    self.message("Humidity: %f" % (data["humidity"]))
                if (data["humidityTemperatureValid"]):
                    self.message("Humidity temperature: %f" % (data["humidityTemperature"]))
                time.sleep(poll_interval*1.0/1000.0)
            except KeyboardInterrupt:
                self.gentle_close()
                break

        else:
            self.gentle_close()
#/////////////////////////////////leveler

    def leveler(self):
        sense.clear()
        sense.set_pixels(redimage)
        self.Threader(self.Manual)
        while self.run==True:
            try:
                raw = sense.accel_raw
                x = raw["x"]
                y = raw["y"]
                z = raw["z"]
                print (x,y,z)

                if (-0.02 < x < 0.02) and (-0.02 < y < 0.02) and (0.98 < z < 1.02):
                    sense.set_pixels(whiteimage)
                elif (-0.02 < x < 0.02) and (-0.90 > y > -1.1):
                    sense.set_pixels(greenimage)
                elif (-0.02 < y < 0.02) and (-0.90 > x > -1.1):
                    sense.set_pixels(blueimage)
                else:
                    sense.set_pixels(redimage)
            except KeyboardInterrupt:
                self.gentle_close()
                break
        else:
            self.gentle_close()
#//////////////////////////////////////live balancer
            
    def balancer(self):
        global game_over
        def move_marble(pitch,roll,x,y):
            new_x = x
            new_y = y
            if 10 < pitch < 170 and x != 0:
                new_x -= 1
            elif 350 > pitch > 170 and x != 7 :
                new_x += 1
            if 10 < roll < 170 and y != 7:
                new_y += 1
            elif 350 > roll > 170 and y != 0 :
                new_y -= 1
            x,y = check_wall(x,y,new_x,new_y)
            return x,y

        def check_wall(x,y,new_x,new_y):
            if maze[new_y][new_x] != r:
                return new_x, new_y
            elif maze[new_y][x] != r:
                return x, new_y
            elif maze[y][new_x] != r:
                return new_x, y
            else:
                return x,y

        '''def check_win(x,y):
            global game_over
            if maze[y][x] == g:
                game_over = True
                sense.show_message('You Win')
                import Saving_Grace
                sys.exit()'''
        self.Threader(self.Manual)
      
        while self.run==True:#not game_over:
            try:
                pitch = sense.get_orientation()['pitch']
                roll = sense.get_orientation()['roll']
                x,y = move_marble(pitch,roll,x,y)
                #check_win(x,y)
                maze[y][x] = w
                sense.set_pixels(sum(maze,[]))
                sleep(0.01)
                maze[y][x] = b
            except KeyboardInterrupt:
                sense.clear()
                game_over=True
                self.gentle_close()
                break
        else:
            self.gentle_close()
#////////////////////////////////////////////gps

    def runGPS(self):
            sense = SenseHat()
            sense.clear()
            sense.set_rotation(90)

            the_connection = gps3.GPSDSocket()
            the_fix = gps3.Fix()

            finalLat = 0
            finalLong = 0

            #Get the Latitude and Longitude
            try:
               for new_data in the_connection:
                  if new_data:
                    the_fix.refresh(new_data)
                  if not isinstance(the_fix.TPV['lat'], str):  # check for valid data
                    latitude = the_fix.TPV['lat']
                    longitude = the_fix.TPV['lon']
                    finalLat = latitude
                    finalLong = longitude
                    time.sleep(1)
                    self.gentle_close()
                    break
            except KeyboardInterrupt:
               self.gentle_close()
               the_connection.close()
               print("\nTerminated by user\nGood Bye.\n")

            latString = ""
            longString = ""

            if finalLat < 0:
               latString = "Lat: " + str(abs(finalLat)) +  " S"
            else: 
               latString = "Lat: " + str(finalLat) + " N"

            if finalLong < 0:
               longString = "Long: " + str(abs(finalLong)) + " W"
            else: 
               longString = "Long: " + str(finalLong) + " E"

            sense.show_message(latString + " " + longString,scroll_speed=.04)
            
#////////////////////////////////freefaller
# Create a variable to store whether or not we're logging data
#running = False # No data being recorded (yet)
    def Faller(self):
#freefaller
# Use the logging library to handle all our data recording
        logfile = "gravity-"+str(datetime.now().strftime("%Y%m%d-%H%M"))+".csv"
        # Set the format for the timestamp to be used in the log filename
        logging.basicConfig(filename=logfile, level=logging.DEBUG,
            format='%(asctime)s %(message)s')
        running = True#false # No data being recorded (yet)
        try:
            print('Press the Joystick button to start recording.')
            print('Press it again to stop.')
            self.Threader(self.Manual)
            while self.run==True:
                # capture all the relevant events from joystick
                r,w,x=select([dev.fd],[],[],0.01)
                for fd in r:
                    for event in dev.read():
                        # If the event is a key press...
                        if event.type==ecodes.EV_KEY and event.value==1:
                            # If we're not logging data, start now
                            if event.code==ecodes.KEY_ENTER and not running:
                                running = True # Start recording data
                                sense.clear(0,255,0) # Light up LEDs green 
                            # If we were already logging data, stop now
                            elif event.code==ecodes.KEY_ENTER and running:
                                running = False
                                gentle_close()
                # If we're logging data...
                if running:
                    self.anime("/home/pi/Desktop/NAVI/SPIRIT/WANDER_LUST/memory/media/FREEFALL/")
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
                     # Read from acceleromter
                    acc_x,acc_y,acc_z = [sense.get_accelerometer_raw()[key] for key in ['x'
        ,'y','z']]
                    # Format the results and log to file
                    logging.info('{:12.10f}, {:12.10f}, {:12.10f}'.format(acc_x,acc_y,acc_z))
                    print(acc_x,acc_y,acc_z) # Also write to screen
        #except: # If something goes wrong, quit
            #gentle_close()
        except KeyboardInterrupt:
            self.gentle_close()

        else:
            self.gentle_close()

#////////////////////////////main
    def set_pixels(self,pixels, col):
        for p in pixels:
            sense.set_pixel(p[0], p[1], col[0], col[1], col[2])

    def handle_code(self,code, colour):
        if code == ecodes.KEY_RIGHT:
            self.set_pixels(RIGHT_PIXELS, colour)
            self.run=False
            self.gentle_close()
            
    def Manual(self):
        try:
            if self.run=True:
                for event in dev.read_loop():
                    if event.type == ecodes.EV_KEY:
                        if event.value == 1:  # key down
                            self.handle_code(event.code, white)
            except KeyboardInterrupt:
                sys.exit()

M=Master()
#M.Manual()
#M.balancer
#M.leveler()
#M.Faller()

#M.compass()
#M.runGPS()

#M.HeatFinder()
#M.HumidFinder()
#M.atmos()
#add time now TO 
#exceptions for red xs
