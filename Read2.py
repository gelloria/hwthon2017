#!/usr/bin/env python
# -*- coding: utf8 -*-

#import json
#from httplib2 import Http
import urllib2
import urllib
#from urllib import urlencode

import RPi.GPIO as GPIO
import time ## Import 'time' library.  Allows us to use 'sleep'
import MFRC522
import signal


continue_reading = True
url = "http://192.34.59.148:3000/position"
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT) ## Setup GPIO pin 7 to OUT

## Define function named Blink()
def Blink(numTimes, speed):
    for i in range(0,numTimes): ## Run loop numTimes
        #print "Iteration " + str(i+1) ##Print current loop
        GPIO.output(7, True) ## Turn on GPIO pin 7
        time.sleep(speed) ## Wait
        GPIO.output(7, False) ## Switch off GPIO pin 7
        time.sleep(speed) ## Wait
        #print "Done" ## When loop is complete, print "Done"
    #GPIO.cleanup()


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
#print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."



# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
        #Blink(int(5),float(0.05))
        
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])#+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
               
        
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
            Blink(int(5),float(0.05))
            #h = Http()
            query_args={"TYPE": "4","U_ID": str(uid[0]),"POS": "1"}
            data=urllib.urlencode(query_args)
            request= urllib2.Request(url,data)
            #print "hola mundo"
            response= urllib2.urlopen(request).read()
            #print "hola mundo2"
            #print response

            
            #prueba = json
            #resp,content = h.request(url,"POST",urlencode(prueba))
        else:
            print "Authentication error"

        

