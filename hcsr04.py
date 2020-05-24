import RPi.GPIO as gpio
import time

class ultrasonic:
    def __init__(self, trig, echo):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        self.trig = trig
        self.echo = echo
        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)
        gpio.output(self.trig,False)
        time.sleep(1)

    def getTimeCM(self):
        distanceSum = 0

        #here This loop is to take 25 reading and get the average
        #there the plenty of resources which explain how it works like
        #https://pythonprogramming.net/gpio-input-raspberry-pi-tutorials/?completed=/gpio-raspberry-pi-tutorials/
        for i in range (25):
            gpio.output(self.trig, True)
            time.sleep(0.00001)
            gpio.output(self.trig, False)

            #used try because once a while I was getting some UnboundLocalError
            #if you can check this it would be a great help
            try:
                while gpio.input(self.echo) == 0:
                    start = time.time()

                while gpio.input(self.echo) == 1:
                    end = time.time()

                pulse = end - start

                distance = pulse / 0.000058
                distanceSum += round(distance, 1)

            except UnboundLocalError:
                pass

            time.sleep(0.001)

        return distanceSum/25       #return the average distance
