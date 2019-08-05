from sense_hat import SenseHat

sense = SenseHat()
def leveler():
    sense.clear()
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

    sense.set_pixels(redimage)
    while True:
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
            break
