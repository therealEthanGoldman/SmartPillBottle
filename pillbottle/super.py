
import os
from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

i = 0
j = 0
k = 0
restarting = False
while True:
        
    if (GPIO.input(23)==True):
        restarting = False
    else:            
        # do over print "Light"
        if (restarting == False):
            restarting = True
			
					
        sleep(1);
        
        
        

