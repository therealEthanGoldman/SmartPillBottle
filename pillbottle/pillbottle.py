#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Basic imports
import os
import sys
import smtplib
import Logger
import dbSettings

from time import sleep
from email.mime.text import MIMEText

#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain
from Phidgets.Phidget import PhidgetLogLevel

# import for GPIO
import RPi.GPIO as GPIO

class Buzzer(object):
 def __init__(self):
  GPIO.setmode(GPIO.BCM)  
  self.buzzer_pin = 5 #set to GPIO pin 5
  GPIO.setup(self.buzzer_pin, GPIO.IN)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  print("buzzer ready")

 def __del__(self):
  class_name = self.__class__.__name__
  print (class_name, "finished")

 def buzz(self,pitch, duration):   #create the function “buzz” and feed it the pitch and duration)
 
  if(pitch==0):
   sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave  
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):    #start a loop from 0 to the variable “cycles” calculated above
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   sleep(delay)    #wait with pin 18 low

 def play(self, tune):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0

  print("Playing tune ",tune)
  if(tune==1):
    pitches=[262,294,330,349,392,440,494,523, 587, 659,698,784,880,988,1047,1200,2048]
    duration=0.1
    for p in pitches:
      self.buzz(p, duration)  #feed the pitch and duration to the function, “buzz”
      sleep(duration *0.5)
    for p in reversed(pitches):
      self.buzz(p, duration)
      sleep(duration *0.5)

  elif(tune==2):
    pitches=[262,330,392,523,1047]
    duration=[0.2,0.2,0.2,0.2,0.2,0,5]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the function, “buzz”
      sleep(duration[x] *0.5)
      x+=1
  elif(tune==3):
    pitches=[392,294,0,392,294,0,392,0,392,392,392,0,1047,262]
    duration=[0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      sleep(duration[x] *0.5)
      x+=1

  elif(tune==4):
    pitches=[1047, 988,659]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      sleep(duration[x] *0.5)
      x+=1

  elif(tune==5):
    pitches=[1047, 988,523]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      sleep(duration[x] *0.5)
      x+=1
  elif(tune==6):
      pitches=[392,294,0]
      duration=[0.1,0.1,0.1]
      for p in pitches:
          self.buzz(p, duration[x])
          sleep(duration[x]*0.5)
          x+=1

  GPIO.setup(self.buzzer_pin, GPIO.IN)
# end buzzer class

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(16, False)
GPIO.output(20, False)
GPIO.output(21, False)

buzzer = Buzzer()
logger = Logger.Logger()
mySettings = dbSettings.dbSettings()

me = 'iotlab01@gmail.com'

def appexit(retcode):
    GPIO.cleanup()
    MailClose(theServer)
    exit(retcode)


def MailInit():
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(me,'IOTlab0000')
    return s

def MailClose(svr):
    svr.close()

def Mailtime(svr, messageText, subject, recipient):
    msg = MIMEText(messageText)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = recipient
    svr.sendmail(me, [recipient], msg.as_string())

#Create a bridge object
try:
    bridge = Bridge()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

theServer = MailInit()

#lidstuff
# add code to get default empty weight from DB
#
# starting expected full bottle weight
detailedloggingon = False
oldweight = 2.721800
# no bottle weight
nobottleweight = 2.5104
#empty bottle weight with lid
emptyweight = 2.6118
pillweight = 0.0026
weightsum = 0.0
count = 0
currentweight = oldweight
newweight = currentweight
oldpills = 0
islidopen = False
skipone = False
GPIO.output(20, True)
GPIO.output(21, False)

#Event Handler Callback Functions
def aveweight(e):
    global oldweight
    global currentweight
    global newweight
    global islidopen
    global weightsum
    global count
    global oldpills
    global skipone
    if (GPIO.input(24)==True):
        GPIO.output(16, True)
        buzzer.play(6)
    if (e.value > (emptyweight-pillweight)):
      count = count + 1
      weightsum = weightsum + e.value
      totalpills = round((currentweight - emptyweight)/pillweight+0.5, 0)
      justclosed = False
    
      if (GPIO.input(24)==True):
        skipone = True
        closed = False
        if islidopen == False:
            oldweight = currentweight
            oldpills = totalpills
            islidopen = True
      elif islidopen == True:
        closed = True
        GPIO.output(16, False)
      else:
        islidopen = False
        closed = True

      if count == 4:
        count = 0
        newweight = weightsum/4
        weightsum = 0.0
        # save to log?
        if (newweight < (emptyweight - pillweight)):
            ignoreflag = True
        else:
            ignoreflag = False
            currentweight = newweight
            # add code for newweight or weight changes here
            if skipone == False:
                islidopen = True
                justclosed = True
            else:
                skipone = False
            if justclosed:
                totalpills = round((currentweight - emptyweight)/pillweight+0.5, 0)
                if totalpills > oldpills:
                    logger.logEvent(" %i pills were added" % (totalpills - oldpills))
                    oldpills = totalpills
                elif totalpills < oldpills:
                    taken = oldpills - totalpills
                    # get patient name, caregiver email and dose from DB
                    # if taken is more than dose email Caregiver
                    dose = int(mySettings.getSetting(4))
                    patientname = "The ImPatient"
                    patientname = mySettings.getSetting(3)
                    caregiveremail = 'ethan_goldman@student.uml.edu'
                    caregiveremail = mySettings.getSetting(1)
                    msgTxt = "The patient %s took too many pills. %i instead of %i" % (patientname, taken, dose)
                    sbjctText = "CAREGIVER: A patient took too much warning"
                    if taken > dose:
                        Mailtime(theServer, msgTxt, sbjctText, caregiveremail)
                    logger.logEvent(" %i pills were taken" % (taken))
                    oldpills = totalpills
        if detailedloggingon:
            print("Ave weight: %f num pils: %i" % (currentweight, totalpills))

def BridgeAttached(e):
    attached = e.device
    print("Bridge %i Attached!" % (attached.getSerialNum()))

def BridgeDetached(e):
    GPIO.output(20, False)
    GPIO.output(21, True)
    detached = e.device
    print("Bridge %i Detached!" % (detached.getSerialNum()))

def BridgeError(e):
    try:
        GPIO.output(20, False)
        GPIO.output(21, True)
        source = e.device
        print("Bridge %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (bridge.isAttached(), bridge.getDeviceName(), bridge.getSerialNum(), bridge.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of bridge inputs: %i" % (bridge.getInputCount()))
    print("Data Rate Max: %d" % (bridge.getDataRateMax()))
    print("Data Rate Min: %d" % (bridge.getDataRateMin()))
    print("Input Value Max: %d" % (bridge.getBridgeMax(0)))
    print("Input Value Min: %d" % (bridge.getBridgeMin(0)))

#Main bridge code
try:
	#logging example, uncomment to generate a log file
    #bridge.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")
	
    bridge.setOnAttachHandler(BridgeAttached)
    bridge.setOnDetachHandler(BridgeDetached)
    bridge.setOnErrorhandler(BridgeError)
    bridge.setOnBridgeDataHandler(aveweight)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    GPIO.output(20, False)
    GPIO.output(21, True)
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    bridge.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    GPIO.output(20, False)
    GPIO.output(21, True)
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    bridge.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        GPIO.output(20, False)
        GPIO.output(21, True)
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    GPIO.output(20, False)
    GPIO.output(21, True)
    print("Exiting....")
    appexit(1)
else:
    displayDeviceInfo()

try:
    print("Set data rate to 8ms ...")
    bridge.setDataRate(250)
    sleep(2)

    print("Set Gain to 8...")
    bridge.setGain(0, BridgeGain.PHIDGET_BRIDGE_GAIN_8)
    sleep(2)

    print("Enable the Bridge input for reading data...")
    bridge.setEnabled(0, True)
    sleep(2)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        GPIO.output(21, False)
        GPIO.output(20, True)
        appexit(1)
    GPIO.output(20, False)
    GPIO.output(21, True)
    print("Exiting....")
    appexit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    print("Disable the Bridge input for reading data...")
    bridge.setEnabled(0, False)
    sleep(2)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        GPIO.output(21, False)
        GPIO.output(20, True)
        print("Exiting....")
        appexit(1)
    print("Exiting....")
    appexit(1)

try:
    bridge.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    appexit(1)

print("Done.")
GPIO.cleanup()
MailClose(theServer)
exit(0)
