import sensor, image, time, pyb, csv
from pyb import LED
from pyb import UART
from pyb import I2C

##################################################
# Helper function to convert the RTC input to
# human readable string
##################################################
def bcdDigits(self, chars):
    for char in chars:
    #    char = ord(char)
        for val in (char >> 4, char & 0xF):
            if val==0xF:
                return
            return val


##################################################
#TODO implement this function
#this function initializes all GPIO
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initGPIO(self)
    PIR_init=pyb.Pin("P3", pyb.Pin.OUT_PP)
    PowSw_init=pyb.Pin("P4", pyb.Pin.IN, pyb.Pin.PULL_DOWN)
    return True
##################################################
#TODO implement this function
#this function initializes all timers
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initTimers(self):


##################################################
#TODO implement this function
#this function initializes UART protocol
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initUART(self):
    try:
        uart = UART(1)
        uart.init(9600, bits = 8, parity = None, stop = 1, timeout_char = 1000)    
    except ValueError:
        print("Error: baud rate +- 5% out of range")
##################################################
#TODO implement this function
#this function initializes I2C protocol
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initI2C(self):
    i2c = I2C(2, I2C.MASTER, baudrate=100000)

##################################################
#TODO implement this function
#this function initializes interrupt for the timer
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initInterruptTimer(self):


##################################################
#TODO implement this function
#this function initializes interrupt for the UART
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initInterruptPIR(self):


##################################################
#TODO implement this function
#this function enters the microcontroller into low power mode
#
#returns false upon failure
#returns true upon success
##################################################
def enterLowPowerMode(self):


##################################################
#TODO implement this function
#this function wakes the microcontroller up from sleep
#
#returns false upon failure
#returns true upon success
##################################################
def wakeup(self):

##################################################
#TODO implement this function
#this function reads the PIR sensor from GPIO
#
#returns true upon sensing movement
#returns false upon no movement
##################################################
def readPIR(self):


##################################################
#TODO implement this function
#this function writes the time to the PIR sensor
#
#param time a string for the current time of day
#returns void
##################################################
def writePIR(self, time):


##################################################
#TODO implement this function
#this function reads the RFID module and will
#return a string based on the tag read or if no
#tag is read then a null string will be returned
#
#returns a string with the tag id or a null string
##################################################
def readRFID(self):


##################################################
#TODO implement this function
#this function reads the real time clock for the
#current time of day and the date
#
#returns a string with the time and date
##################################################
def readRTC(self):


##################################################
#TODO implement this function
#this function takes one image from the camera and
#saves it to the SD card memory in the micro
#
#returns false upon failure of storage of photo
#returns true upon success of storage of photo
##################################################
def takePhoto(self):


##################################################
#TODO test this function against tagData.csv
#TODO add error checking
#this function adds a row to the CSV file based on
#the input parameters given
#
#param dateTime string for the date and time
#param tagID string for the 15 digit tag id
#param photoCount string for the number of photos
#returns false upon file edit failure
#returns true upon file edit success
##################################################
def addRowToCSV(self, dateTime, tagID, photoCount):
    fields=[dateTime, tagID, photoCount]
    with open('./tagData.csv', 'a') as fd:
        fd.writerow(fields)


##################################################
#TODO implement this function
#this function enables the GPIO interrupt
##################################################
def enableInterruptGPIO(self):


##################################################
#TODO implement this function
#this function disables the GPIO interrupt
##################################################
def disableInterruptGPIO(self):


##################################################
#TODO implement this function
#this function enables the timer interrupt
##################################################
def enableInterruptTimer(self):


##################################################
#TODO implement this function
#this function disables the timer interrupt
##################################################
def disableInterruptTimer(self):


##################################################
#TODO implement this function
#this function reads the JSON file from the SD
#card and sets the values read to local variables
#
#returns false upon unsuccessful read
#returns true upon successful read
##################################################
def readJSON(self):

