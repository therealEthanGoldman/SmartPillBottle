#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO   #import the GPIO library
import datetime                #import the time library
import MySQLdb


class Logger(object):
    def __init__(self):
        self.db = MySQLdb.connect(host="127.0.0.1",      # host, usually localhost
                         user="root",           # username
                         passwd="p3gasus",      # password
                         db="iotdevdb")           # name of the database
        self.cursor = self.db.cursor()
    
    def __del__(self):
        class_name = self.__class__.__name__
        # disconnect from server
        self.db.close()
        print (class_name, "finished")

    def logEvent(self, eventtext):
        devname = "EthansPi"
        curdt = datetime.datetime.now()
        #SQL query to INSERT a record into the table iotlog.
        self.cursor.execute('''INSERT into iotlog (ldate, ltime, devname, logentry)
                  values (%s, %s, %s, %s)''',
                  (curdt.date(), curdt.time(), devname, eventtext))
        # Commit your changes in the database
        self.db.commit()

if __name__ == "__main__":
  logger = Logger.Logger()
  	

        
        

		    

