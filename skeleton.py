import sensor, image, time, pyb, csv, json
from pyb import LED
from pyb import UART
from pyb import I2C


##################################################
# Global Variables
##################################################
pinPIR = null
pinPowerSwitch = null
uartObject = null
strDateTime[] = null
pinI2C = null

#Configuration variables set to default values
#TODO: add the rest of the config variables and
#TODO: set them to their proper default values
burstCount = 3


##################################################
# Helper function to convert the RTC input to
# human readable string
##################################################
def bcdDigits(chars):
    for char in chars:
    #    char = ord(char)
        for val in (char >> 4, char & 0xF):
            if val==0xF:
                return
            return val


##################################################
#TODO implement error checking
#this function initializes all GPIO
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initGPIO():
    global pinPIR
    global pinPowerSwitch

    pinPIR = pyb.Pin("P3", pyb.Pin.OUT_PP)
    pinPowerSwitch = pyb.Pin("P4", pyb.Pin.IN, pyb.Pin.PULL_DOWN)
    return True


##################################################
#TODO implement this function
#this function initializes all timers
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initTimers():


##################################################
#this function initializes UART protocol
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initUART():
    global uartObject

    try:
        #UART(1) uses pins 0 and 1
        uartObject = UART(1) 
        uartObject.init(9600, bits = 8, parity = None, stop = 1, timeout_char = 1000)    
    except ValueError:
        # print("Error: baud rate +- 5% out of range")
        return False
    
    return True


##################################################
#TODO implement this function
#this function initializes I2C protocol
##################################################
def initI2C():
    global pinI2C

    #2 wire I2C communication, SCL = P4, SDA = P5
    pinI2C = I2C(2, I2C.MASTER, baudrate=100000)


##################################################
#TODO implement this function
#this function initializes interrupt for the timer
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initInterruptTimer():


##################################################
#TODO implement this function
#this function initializes interrupt for the UART
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initInterruptPIR():


##################################################
#TODO implement this function
#this function enters the microcontroller into low power mode
#
#returns false upon failure
#returns true upon success
##################################################
def enterLowPowerMode():


##################################################
#TODO implement this function
#this function wakes the microcontroller up from sleep
#
#returns false upon failure
#returns true upon success
##################################################
def wakeup():


##################################################
#this function reads the PIR sensor from GPIO
#
#returns true upon sensing movement
#returns false upon no movement
##################################################
def readPIR():
    global pinPIR

    if pinPIR.value() == 1:
        return True
    else:
        return False
        

##################################################
#TODO hardcode actual time/date
#this function writes the time to the PIR sensor
#hard code time/date values
#
#returns void
##################################################
def writeRTC():
    global pinI2C

    pinI2C.mem_write(0x00,0x68,0, timeout=1000)
    pinI2C.mem_write(0x04,0x68,1, timeout=1000)
    pinI2C.mem_write(0x15,0x68,2, timeout=1000)
    pinI2C.mem_write(0x03,0x68,3, timeout=1000)
    pinI2C.mem_write(0x17,0x68,4, timeout=1000)
    pinI2C.mem_write(0x05,0x68,5, timeout=1000)
    pinI2C.mem_write(0x19,0x68,6, timeout=1000)

##################################################
#TODO parse strDateTime indexes to make human
# sense
#this function reads the real time clock for the
#current time of day and the date
#
#returns a string with the time and date
##################################################
def readRTC():
    global strDateTime

    for i in range (0,7):
        #read the full data from RTC address
        readFirst = (pinI2C.mem_read(1, 0x68, 0))
        #parse the ones and tens place of the data
        readParse = (ord(readFirst) & 0x0F)
        strDateTime[i] = "" + readParse + bcdDigits(readFirst)

    #form strDateTime into string:
    # yyyy-MM-dd hh-mm-ss (all numbers)
    # return that^ string


##################################################
#TODO test read buffer length that is required
#this function reads the RFID module and will
#return a string based on the tag read or if no
#tag is read then a null string will be returned
#
#returns a string with the tag id or a null string
##################################################
def readRFID():
    return uartObject.read(60)


##################################################
#TODO implement error checking
#this function toggles the power to the RFID
#
#returns 1 if it set it to high
#returns 0 if it set it to low
##################################################
def powerToggleRFID():
    if pinPowerSwitch.value() == 1:
        pinPowerSwitch.low()
        return 0
    else:
        pinPowerSwitch.high()
        return 1



##################################################
#TODO implement this function
#this function takes one image from the camera and
#saves it to the SD card memory in the micro
#
#returns false upon failure of storage of photo
#returns true upon success of storage of photo
##################################################
def takePhoto():


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
def addRowToCSV(dateTime, tagID, photoCount):
    fields=[dateTime, tagID, photoCount]
    with open('./tagData.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    return True


##################################################
#TODO implement this function
#this function enables the GPIO interrupt
##################################################
def enableInterruptGPIO():


##################################################
#TODO implement this function
#this function disables the GPIO interrupt
##################################################
def disableInterruptGPIO():


##################################################
#TODO implement this function
#this function enables the timer interrupt
##################################################
def enableInterruptTimer():


##################################################
#TODO implement this function
#this function disables the timer interrupt
##################################################
def disableInterruptTimer():


##################################################
#TODO complete setting global variables
#TODO add error checking
#this function reads the JSON file from the SD
#card and sets the values read to local variables
#
#returns false upon unsuccessful read
#returns true upon successful read
##################################################
def readJSON():
    fileJSON = './configuration.json'
    global burstCount

    with open(fileJSON, 'r') as f:
        readData = json.load(f)

    burstCount = readData["burstCount"]