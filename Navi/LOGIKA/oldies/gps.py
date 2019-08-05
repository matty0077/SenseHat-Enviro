#sys.path.append("/home/pi/Desktop/NAVI/WANDER_LUST/memory/Navi")#to import files from another folder

from sense_hat import SenseHat
from time import sleep
import gps3

#Class to get the Latitude and Longitude
def runGPS():
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
                sleep(1)
                break
        except KeyboardInterrupt:
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




runGPS()
