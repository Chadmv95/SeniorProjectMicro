import sensor, image, time, pyb, ujson, uos
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
global pirFlag
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

    pinPIR = pyb.ExtInt("P3", pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, callback=handlePIR)
    pinPowerSwitch = pyb.Pin("P6", pyb.Pin.OUT_PP)


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
#this function initializes I2C protocol
##################################################
def initI2C():
    global pinI2C
    #2 wire I2C communication, SCL = P4, SDA = P5
    pinI2C = I2C(2, I2C.MASTER, baudrate=100000)


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
#this function reads the real time clock for the
#current time of day and the date and sets the
#global variable
##################################################
def readRTC():
    global strDateTime
    global arrDateTime
    strDateTime = ""

    for i in range (0,7):
        #read the full data from RTC address
        readFirst = (pinI2C.mem_read(1, 0x68, (6-i)))

        #parse the ones and tens place of the data
        readParse = (ord(readFirst) & 0x0F)
        arrDateTime[i] = ""  + str(bcdDigits(readFirst))+ str(readParse)

        # yy-MM-dd hh-mm-ss (all numbers)
        strDateTime += ("" + str(arrDateTime[6-i]) )

##################################################
#this function reads the real time clock on the
#actual board and returns a string for the time
##################################################
def readTime():
    global rtc
    unCleanTime = rtc.datetime()
    cleanTime = [0,0,0,0,0,0]

    for i in range (0,6):
        if i<3:
            cleanTime[i] = unCleanTime[i]
        else:
            cleanTime[i] = unCleanTime[i+1]
    return cleanTime


##################################################
#this function reads the RFID module and will
#return a string based on the tag read or if no
#tag is read then a null string will be returned
#
#returns a string with the tag id or a null string
##################################################
def readRFID():
    global uartObject
    uartObject.write("RAT\r")
    read = uartObject.read(60)
    return read


##################################################
#this function toggles the power to the RFID
#
#returns 1 if it set it to high
#returns 0 if it set it to low
##################################################
def powerToggleRFID():
    global pinPowerSwitch
    if pinPowerSwitch.value() == 1:
        pinPowerSwitch.low()
        return 0
    else:
        pinPowerSwitch.high()
        return 1


##################################################
#this function takes one image from the camera and
#saves it to the SD card memory in the micro
#
#returns void
##################################################
def takePhoto(filename):
    sensor.snapshot().save(filename)


##################################################
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
    #expect datetime to be a string list
    dateTime = str(dateTime).replace(",", "_")
    with open('timestamps.csv', 'a') as timeFile:
        timeFile.write(dateTime + "," + str(tagID) + "," + str(photoCount) + "\n")

    return True


##################################################
#this function enables the PIR interrupt
##################################################
def enableInterruptPIR():
    global pinPIR
    pinPIR.enable()

##################################################
#this function disables the PIR interrupt
##################################################
def disableInterruptPIR():
    global pinPIR
    pinPIR.disable()

##################################################
#this function enables the timer interrupt
##################################################
def enableInterruptTimer( wakeTime ):
    global rtc
    rtc.wakeup(wakeTime, handleTimer)

##################################################
#this function disables the timer interrupt
##################################################
def disableInterruptTimer():
    enableInterruptTimer(None)


##################################################
#this function enables the RTC interrupt
#
#param wakeTime milliseconds to trigger interrupt
##################################################
def enableInterruptRTC( wakeTime ):
    global rtc
    rtc.wakeup(wakeTime, handleRTC)


##################################################
#this function disables the RTC interrupt
##################################################
def disableInterruptRTC():
    enableInterruptRTC(None)


##################################################
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
#it takes a photo and creates/names the directory
##################################################
def handleRTC(line):
    global totalPhotoCount
    global photoNum

    list_timestamp = str(list(timestamp))
    list_timestamp = str(list_timestamp).replace(",", "_")
    new_dir = "Photos/" + list_timestamp

    try:
        uos.stat(new_dir)
    except OSError:
        uos.mkdir(new_dir)

    photoName = new_dir + "/" + list_timestamp + "_" + str(totalPhotoCount)
    takePhoto(photoName)
    totalPhotoCount += 1


##################################################
#this function handles the PIR interrupt
#it sets a flag for the while loop in the main
##################################################
def handlePIR(line):
    global pirFlag
    pirFlag = True


##################################################
#this function handles the timer interrupt
#it sets a flag for the while loop in the main
##################################################
def handleTimer(line):
    global timerFlag
    timerFlag = True


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
    initCameraSensor()
    initGPIO()
    initI2C()
    initUART()

    #read the time from the timer and store it on the micro
    readRTC()
    rtc.datetime((int("20"+arrDateTime[0]),
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
    enableInterruptPIR()

    #enter low power mode
    timerFlag = True
    pirFlag = False
    green_led = pyb.LED(2)
    green_led.on()
    pyb.delay(50000)
    green_led.off()

    enterLowPowerMode()

    #this while loop just has the system wait so the
    #program does not terminate while it waits for the
    #interrupt to occur from the IR sensor

    while(1):
        if timerFlag == True:
            #allow the PIR to be triggered again
            enableInterruptPIR()

            #check for trigger
            if pirFlag == True:
                disableInterruptPIR()
                readAgain = True
                tempTagID = 0
                tagID = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                num_loops = 0
                photoNum = 0
                timestamp = readTime()
                initCameraSensor()
                #list_timestamp = str(list(timestamp))
                #new_dir = "Photos/" + list_timestamp

                #try:
                    #uos.stat(new_dir)
                #except OSError:
                    #uos.mkdir(new_dir)

                #takePhoto(new_dir + "/" + list_timestamp + "_" + "0")

                #we have read the tag, don't care if it didn't work
                #start taking photos, we can read later
                powerToggleRFID()

                #spend the first 3 seconds reading
                while(readAgain and num_loops < 3):
                    TempTagID = readRFID()

                    if TempTagID == b'?1\r' or TempTagID == "" or TempTagID == None or TempTagID == b'\x00':
                        readAgain = True
                    else:
                        readAgain = False
                    num_loops += 1

                powerToggleRFID()
                enableInterruptRTC(burstTime*1000)

                #make sure the tag is legit
                #if it is legit, format it so it is readable
                if TempTagID is not None:

                    if len(TempTagID) == 18:
                        for i in range (0,16):
                            tagID[i] = chr(TempTagID[i+1])
                    elif len(TempTagID) == 20:
                        for i in range (0,16):
                            tagID[i] = chr(TempTagID[i+3])
                    elif len(TempTagID) > 4:
                        for i in range (0,16):
                            tagID[i] = chr(TempTagID[i])
                    else:
                            tagID = "NoTag"
                    tagID = "".join(tagID)
                else:
                    tagID = "RFID Module Error"
                #print(tagID)
                #print(TempTagID)
                while totalPhotoCount < burstCount:
                    pass

                totalPhotoCount = 0
                #add the data we collected
                addRowToCSV(timestamp, tagID, burstCount)

                #cleanup and get ready to go back to low power mode
                disableInterruptRTC()
                pirFlag = False

                #prepare the powersavertimeout timer
                enableInterruptTimer(powerSaverTimeout*1000)
                timerFlag = False
                blue_led = pyb.LED(3)
                blue_led.on()
                pyb.delay(1000)
                blue_led.off()
                #print("testing")
                TempTagID=b'x00'
                tagID = b'x00'
                readRFID()
                enterLowPowerMode()

