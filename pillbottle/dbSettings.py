#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO   #import the GPIO library
import datetime                #import the time library
import MySQLdb


class dbSettings(object):
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

    def getSetting(self, setting):
        #SQL query to select the setting from the settings table.
        self.cursor.execute('''select * from settings ''')
        # Commit your changes in the database
        self.db.commit()
        row = self.cursor.fetchone()
        return row[setting]
		
    def setSetting(self, setting, value):
        #SQL query to select the setting from the settings table.
        self.cursor.execute('''update settings SET ``%s`` = ``%s`` ''',
                  (setting, value))
        # Commit your changes in the database
        self.db.commit()
	

if __name__ == "__main__":
  mySettings = dbSettings()
  print(mySettings.getSetting(1))
  print(mySettings.getSetting(3))
  	

        
        

		    

