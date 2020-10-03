# Here in this code I decalared a "setup" and a "loop" function because I have
# just stared using Raspberry Pi GPIO and I am more used to Arduino environment
# so I tried to replicate that. Hope you'll find it interesting.


import RPi.GPIO as gpio     #Importing the GPIO library
from numpy import interp    #This function works exactly same as map function in Arduino
import time                 #For providing delay
import hcsr04               #For hcsr04 sensor class, I wrote it myself


#some basic setup
gpio.setwarnings(False)     #so it wont promt any stupid warnings
gpio.cleanup()              #clean any configured gpio
gpio.setmode(gpio.BCM)      #I'm using the BroadCom pin number system


#define to what pin the led is connected, ledNo:GPIO_Pin
ledpin = {1:27, 2:17, 3:4, 4:5, 5:6, 6:7, 7:8, 8:9, 9:10, 10:11, 11:12, 12:13, 13:14, 14:15, 15:16}

trig = 21               #GPIO_Pin where the trig of the sensor is connected
echo = 20               #GPIO_Pin where the trig of the sensor is connected
setdistance = 0         #set the initial distance of the object for further comarison

ultra1 = hcsr04.ultrasonic(trig, echo)  #creating a hcsr04 object


#defining the setup function
def setup():
    global setdistance
    setdistance = ultra1.getTimeCM()-4      #setting the inital distance of the object

    #setting the led pin as output
    for i in range(1, 16):
        gpio.setup(ledpin[i], gpio.OUT)

    #flashing the led 5 times, just because it looks cool
    for j in range(5):
        for i in range(1, 16):
            gpio.output(ledpin[i], True)
        time.sleep(0.06)
        for i in range(1, 16):
            gpio.output(ledpin[i], False)
        time.sleep(0.06)



#defining the loop function
def loop():
    distance = ultra1.getTimeCM() - 4   #updating the object distance

    #This if statement wont allow the object distance to exceed the inital set distance
    if 0 < distance < setdistance:
        pass
    else:
        distance = setdistance

    #here the arduino map or numpy interp function is used get the number of led
    #to be turned on respect to the position of the object
    led = int(interp(distance, [1, setdistance], [15, 1]))

    #here the resective leds are turned on
    for i in range(1, led+1):
        gpio.output(ledpin[i], True)

    #and the rest are truned off
    for i in range(led, 16):
        gpio.output(ledpin[i], False)





setup()         #here the calling the setup funcion once

try:
    while True:     #and the loop funcion will be called infintly
        loop()

except KeyboardInterrupt:       #use KeyboardInterrupt to stop the program
     GPIO.cleanup()

#bacically here the program first take a inital reading of the position of the
#object and after this the led would turn on proportional to this distance.
#hope its clear
