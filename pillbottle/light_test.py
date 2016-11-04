
import os
from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(16, False)
GPIO.output(20, False)
GPIO.output(21, False)

i = 0
j = 0
k = 0
while True:
        
        if (GPIO.input(23)==False):
                print "Dark"
                GPIO.output(16, True)              
                sleep(1);
                GPIO.output(16, False)
                GPIO.output(20, True)
                sleep(1);
                GPIO.output(20, False)
                GPIO.output(21, True)
                sleep(1);
                GPIO.output(21, False)
                
        if (GPIO.input(23)==True):
                print "Light"
        if (GPIO.input(24)==True):
                print "Hello"
                GPIO.output(16, True)              
                GPIO.output(20, True)
                GPIO.output(21, True)
                sleep(1);
                GPIO.output(21, False)
                GPIO.output(20, False)
                GPIO.output(16, False)


        if (GPIO.input(24)==False):
                print "Goodbye"

        sleep(1);
        
        
        

