import sensor, image, time, pyb, ujson
from pyb import LED
from pyb import UART
from pyb import I2C
from time import sleep

##################################################
# Global Variables
##################################################
global pinPIR
global pinPowerSwitch
global uartObject
global arrDateTime
global pinI2C
global rtc
global totalPhotoCount
#Configuration variables set to default values
global burstCount
global burstTime
global powerSaverTimeout
global triggerInterval
global name
global location


##################################################
# Helper function to convert the rtc input to
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
#initializes camera to the correct settings
#every time it comes out of stop mode, invoke this
##################################################
def initCameraSensor():
    sensor.reset()                         # Reset and initialize the sensor
    sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to b/w 8-bit
    sensor.set_framesize(sensor.VGA)       # Set frame size to 640x480
    sensor.skip_frames()                   # Wait for settings 300ms


##################################################
#this function initializes all GPIO
#it also configures the PIR pin as an interrupt
#
# returns void
##################################################
def initGPIO():
    global pinPIR
    global pinPowerSwitch

    pinPIR = pyb.ExtInt("P3",
                        pyb.ExtInt.IRQ_RISING,
                        pyb.Pin.PULL_DOWN,
                        callback=handlePIR)
    pinPowerSwitch = pyb.Pin("P6", pyb.Pin.OUT_PP)


##################################################
#TODO implement this function
#this function initializes all timers
#
#returns void
##################################################
def initTimers():
    return

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
#TODO add error checking for failure
#this function initializes I2C protocol
#
#returns false upon failure
#returns true upon success
##################################################
def initI2C():
    global pinI2C

    #2 wire I2C communication, SCL = P4, SDA = P5
    pinI2C = I2C(2, I2C.MASTER, baudrate=100000)

    return


##################################################
#TODO implement this function
#this function initializes interrupt for the timer
#
#returns false upon failure of initialization
#returns true upon success of initialization
##################################################
def initInterruptTimer():
    return

##################################################
#this function enters the microcontroller into
# low power mode
#
#returns void
##################################################
def enterLowPowerMode():
    #must configure wakeup sources first
    pyb.stop()
    return


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

    return False


##################################################
#TODO hardcode actual time/date
#this function writes the time to the PIR sensor
#hard code time/date values
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
#TODO test functionality
#this function reads the real time clock for the
#current time of day and the date and sets the
#global variable
##################################################
def readRTC():
    strDateTime = ""

    for i in range (0,7):
        #read the full data from RTC address
        readFirst = (pinI2C.mem_read(1, 0x68, 0))

        #parse the ones and tens place of the data
        readParse = (ord(readFirst) & 0x0F)
        arrDateTime[6-i] = "" + str(readParse) + str(bcdDigits(readFirst))

        # yy-MM-dd hh-mm-ss (all numbers)
        strDateTime += ("" + str(arrDateTime[6-i]) )


##################################################
#TODO figure out the format of the return string
#this function reads the real time clock on the
#actual board and returns a string for the time
##################################################
def readTime():
    return rtc.datetime()


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
#TODO implement error checking and saving to flash
#this function takes one image from the camera and
#saves it to the SD card memory in the micro
#
#returns void
##################################################
def takePhoto(filename):
    sensor.snapshot().save(filename)


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
    with open('timestamps.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    return True


##################################################
#this function enables the PIR interrupt
##################################################
def enableInterruptPIR():
    pinPIR.enable()

##################################################
#this function disables the PIR interrupt
##################################################
def disableInterruptPIR():
    pinPIR.disable()

##################################################
#TODO implement this function
#this function enables the timer interrupt
##################################################
def enableInterruptTimer():
    return

##################################################
#TODO implement this function
#this function disables the timer interrupt
##################################################
def disableInterruptTimer():
    return


##################################################
#this function enables the RTC interrupt
#
#param wakeTime milliseconds to trigger interrupt
##################################################
def enableInterruptRTC( wakeTime ):
    rtc.wakeup(wakeTime, handleRTC)


##################################################
#this function disables the RTC interrupt
##################################################
def disableInterruptRTC():
    enableInterruptRTC(None)


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
    fileJSON = 'configuration.json'
    global burstCount
    global burstTime
    global powerSaverTimeout
    global triggerInterval
    global name
    global location

    with open(fileJSON, 'r') as f:
        readData = ujson.load(f)

    burstCount = readData["Burst Count"]
    burstTime = readData["Burst Time"]
    powerSaverTimeout = readData["Power Saver Timeout"]
    triggerInterval = readData["Trigger Interval"]
    name = readData["Name"]
    location = readData["Location"]


##################################################
#this function handles the RTC interrupt
#it loops and stuff yay!
##################################################
def handleRTC():
    photoName = "/Photos/" + timestamp + "/" + timestamp + "_" + photoNum+1
    takePhoto(photoName)
    totalPhotoCount += 1

##################################################
#this function handles the PIR interrupt
#it loops and stuff yay!
##################################################
def handlePIR():
    print("IM SO TRIGGERED")
    global totalPhotoCount
    readAgain = True
    tagID = 0
    num_loops = 0
    photoNum = 0

    disableInterruptPIR()

    timestamp = rtc.datetime()

    initCameraSensor()
    takePhoto("/Photos/" + timestamp + "/" + timestamp + "_" + 0)

    #we have read the tag, don't care if it didn't work
    #start taking photos, we can read later
    enableInterruptRTC(burstTime*1000)

    #spend the first 3 seconds reading
    while(readAgain and num_loops < 30):
        tagID = readRFID()
        if tagID == "1?":
            readAgain = True
        else:
            readAgain = False
        sleep(0.1)
        num_loops += 1

    #TODO come back to this. instead of doing a no-op
    #TODO in the while loop, optimize the power
    #TODO consumption of tag reading and read the tag
    #TODO as we wait for the photocount to be reached
    while totalPhotoCount < photoCount:
        pass

    #add the data we collected
    addRowToCSV(timestamp, tagID, totalPhotoCount)

    #cleanup and get ready to go back to low power mode
    disableInterruptRTC()
    enableInterruptPIR()
    enterLowPowerMode()
    return


if __name__ == "__main__":

    #Configuration variables set to default values
    pinPIR = None
    pinPowerSwitch = None
    uartObject = None
    arrDateTime = None
    pinI2C = None
    rtc = pyb.RTC()

    totalPhotoCount = 0
    burstCount = 3
    burstTime = 1
    powerSaverTimeout = 3600
    triggerInterval = 1200
    name = "PIT Tracker #1"
    location = "Michigan"
    arrDateTime = [8]*7

    #initialize everything
    # TODO Check for errors
    initCameraSensor()
    initGPIO()
    initI2C()
    initInterruptTimer()
    initTimers()
    initUART()

    #read the time from the timer and store it on the micro
    #TODO verify the date/time params to datetime function
    readRTC()
    rtc.datetime((int(arrDateTime[0]),
                int(arrDateTime[1]),
                int(arrDateTime[2]),
                int(arrDateTime[3]),
                int(arrDateTime[4]),
                int(arrDateTime[5]),
                int(arrDateTime[6]),
                0))

    #read config file and set parameters
    readJSON()

    #enable interrupt for GPIO
    enableInterruptRTC( burstTime * 1000 )
    enableInterruptPIR()

    #enter low power mode
    print("Entering low power mode")
    #enterLowPowerMode()

    #this while loop just has the system wait so the
    #program does not terminate while it waits for the
    #interrupt to occur from the IR sensor
    while(1):
        #print("I am alive!")
        i = 1
