import sys
sys.path.append("/home/pi/Desktop/NAVI/WANDER_LUST")

from sense_hat import SenseHat
sense=SenseHat()
sense.set_rotation(90)
sense.clear()

blue=(0,0,255)
yellow=(255,255,0)
red = (255, 0, 0)
white=(255,255,255)
black=(0,0,0)
green = (0, 255, 0)

def HeatFinder():
    while True:
        try:
            temp = sense.temp
            #print(temp)
            pixels = [red if i < temp else blue for i in range(64)]
            sense.set_pixels(pixels)
        except KeyboardInterrupt:
            sense.clear()
            break

def HumidFinder():
    while True:
        try:
            humidity = sense.humidity
            humidity_value = 64 * humidity / 100
            print(humidity)
            pixels = [green if i < humidity_value else white for i in range(64)]
            sense.set_pixels(pixels)
        except KeyboardInterrupt:
            sense.clear()
            break
