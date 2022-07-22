#!/usr/bin/python3

import os
import cv2
import time
import imutils
import threading
import numpy as np
from signal import pause
from time import sleep
from gpiozero import LED, Button

blink_on = False
interval = 0.1

button1 = Button(5)  # No Filter Button
button2 = Button(6)  # Greyscale Button
button3 = Button(13)  # Sepia Button
button4 = Button(26)  # Shutdown Button
led1 = LED(23)  # Ready Status LED - Green
led2 = LED(24)  # Processing Status LED - Orange

# Multi-Mode Settings Vars
# Mode 0 - Start-up Mode
# Mode 1 - Camera Mode
# Mode 2 - Gallery Mode
# Mode 3 - Null
# Mode 4 - Null
# Mode 5 - Null
# Mode 6 - System Mode

mode = 0

# Selector Switch Vars
Sel0 = Button(25)  # Mode 1
Sel1 = Button(12)  # Mode 2
Sel2 = Button(16)  # Mode 3
Sel3 = Button(17)  # Mode 4
Sel4 = Button(27)  # Mode 5
Sel5 = Button(8)  # Mode 6

# Gallery Vars
currentPhoto = 'null'
previousPhoto = 'null'
nextPhoto = 'null'
lastCapturedPhoto = 'null'

# User Defined Vars
# Device URI mplicitclass://Liene_Photo_Printer_0LF1_USB_/
printerName = 'Liene-Photo-Printer'


def fileNameCheck():
    i = 0
    while os.path.exists(f"/home/pi/image_{i}.jpg"):
        i += 1

    fileName = f"/home/pi/image_{i}.jpg"
    return fileName

## Photo Take Section Start

def sepia(src_image):
    gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32) / 255
    # solid color
    sepia = np.ones(src_image.shape)
    sepia[:, :, 0] *= 153  # B
    sepia[:, :, 1] *= 204  # G
    sepia[:, :, 2] *= 255  # R
    # hadamard
    sepia[:, :, 0] *= normalized_gray  # B
    sepia[:, :, 1] *= normalized_gray  # G
    sepia[:, :, 2] *= normalized_gray  # R
    return np.array(sepia, np.uint8)


def button_NoFilter():
    # Not Used In Code
    # This Is Here For Refrence

    outputFile = fileNameCheck()
    outputCommand = "fswebcam -d /dev/video0 -r 640x480 " + outputFile
    rawFileDirAndName = os.path.splitext(outputFile)[0]
    outputGrey = rawFileDirAndName + '_Grey.jpg'
    outputSepia = rawFileDirAndName + '_Sepia.jpg'
    print('Output File: ' + outputFile)
    print('Output Command: ' + outputCommand)
    print('Output File Greyscale: ' + outputGrey)

    led1.blink(interval, interval)
    os.system(outputCommand)
    print('Photo Taken Check Output Dir')
    print('Applying Monochrome Filter To Photo')
    # Monochrome Filter To Photo
    image = cv2.imread(outputFile)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(outputGrey, gray)
    print('Done Applying Greyscale Filter, Photo Is Located At: ' + outputGrey)
    print('Applying Sepia Filter To Photo')
    # Sepia Filter To Photo
    sepiaImage = sepia(image)
    cv2.imwrite(outputSepia, sepiaImage)
    print('Done Applying Sepia Filter, Photo Is Located At: ' + outputSepia)
    led1.on()
    print('Awaiting User Input...')


def B1():  # No Filter
    print('Taking Photo With No Filter...')
    # Setting Status LED's To Proccessing Mode
    led1.on()
    led2.blink(interval, interval)
    sleep(1)
    # Start Photo Capture
    outputFile = fileNameCheck()
    outputCommand = "fswebcam -d /dev/video0 -r 1920x1080 " + outputFile
    rawFileDirAndName = os.path.splitext(outputFile)[0]
    print('Output File: ' + outputFile)
    print('Output Command: ' + outputCommand)
    os.system(outputCommand)
    print('Photo Taken Check Output Dir')
    global lastCapturedPhoto
    lastCapturedPhoto = outputFile
    #printPhoto(outputFile)
    print('Awaiting User Input...')

    # Set Status LED's Back to Ready Status
    led2.on()
    led1.off()


def B2():  # Greyscale Filter
    print('Taking Photo With Greyscale Filter...')

    # Setting Status LED's To Proccessing Mode
    led1.on()
    led2.blink(interval, interval)
    sleep(1)
    # Start Photo Capture

    outputFile = fileNameCheck()
    outputCommand = "fswebcam -d /dev/video0 -r 1920x1080 " + outputFile
    rawFileDirAndName = os.path.splitext(outputFile)[0]
    outputGrey = rawFileDirAndName + '_Grey.jpg'
    print('Output File: ' + outputFile)
    print('Output Command: ' + outputCommand)
    print('Output File Greyscale: ' + outputGrey)
    os.system(outputCommand)
    print('Photo Taken Check Output Dir')
    print('Applying Monochrome Filter To Photo')
    # Monochrome Filter To Photo
    image = cv2.imread(outputFile)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(outputFile, gray)
    print('Done Applying Greyscale Filter, Photo Is Located At: ' + outputFile)
    global lastCapturedPhoto
    lastCapturedPhoto = outputFile
    #printPhoto(outputFile)
    print('Awaiting User Input...')

    # Set Status LED's Back To Ready Status
    led2.on()
    led1.off()


def B3():  # Sepia Filter
    print('Taking Photo With Sepia Filter...')

    # Setting LED'S to Proccessing Mode
    led1.on()
    led2.blink(interval, interval)
    sleep(1)
    # Start Photo Capure

    outputFile = fileNameCheck()
    outputCommand = "fswebcam -d /dev/video0 -r 1920x1080 " + outputFile
    rawFileDirAndName = os.path.splitext(outputFile)[0]
    outputSepia = rawFileDirAndName + '_Sepia.jpg'
    print('Output File: ' + outputFile)
    print('Output Command: ' + outputCommand)
    os.system(outputCommand)
    # Sepia Filter To Photo
    image = cv2.imread(outputFile)
    sepiaImage = sepia(image)
    cv2.imwrite(outputFile, sepiaImage)
    print('Done Applying Sepia Filter, Photo Is Located At: ' + outputSepia)
    global lastCapturedPhoto
    lastCapturedPhoto = outputFile
    #printPhoto(outputFile)
    print('Awaiting User Input...')

    # Setting LED'S to Ready Mode
    led2.on()
    led1.off()

## Photo Take Section END

def B4():  # Print Photo
    print('Button 4 Pressed...')
    led1.on()
    led2.blink(interval, interval)
    global lastCapturedPhoto
    printPhoto(lastCapturedPhoto)
    led2.on()
    led1.off()

## Gallery Section
    
def showPhoto(photoPath):
    print('Showing Photo...')
    ##os.system('/home/pi/Documents/PyCamSoft/ViewPhoto.py --input ' + photoPath)
    
def closePhoto():
    print('Closing Photo...')
    #cv2.destroyAllWindows()
       
    
## Gallery Section END    



def selector0():
    print('Selector In Position 0')
    global mode
    mode = 1
    print('Mode is ' + str(mode))
    closePhoto()


def selector1():
    print('Selector In Position 1')
    global mode
    mode = 2
    print('Mode is ' + str(mode))
    closePhoto()


def selector2():
    print('Selector In Position 2')
    global mode
    mode = 3
    print('Mode is ' + str(mode))
    closePhoto()


def selector3():
    print('Selector In Position 3')
    global mode
    mode = 4
    print('Mode is ' + str(mode))
    closePhoto()


def selector4():
    print('Selector In Position 4')
    global mode
    mode = 5
    print('Mode is ' + str(mode))
    closePhoto()


def selector5():
    print('Selector In Position 5')
    global mode
    mode = 6
    print('Mode is ' + str(mode))
    closePhoto()
    
def button1press():
    print('Button 1 Pressed...')
    if mode == 1:
        print('Camera Mode...')
        B1()
    if mode == 2:
        print('Gallery Mode...')
    if mode == 3:
        print('Mode Null...')
    if mode == 4:
        print('Mode Null...')
    if mode == 5:
        print('Mode Null...')
    if mode == 6:
        print('System Mode...')
    
def button2press():
    print('Button 2 Pressed...')
    if mode == 1:
        print('Camera Mode...')
        B2()
    if mode == 2:
        print('Gallery Mode...')
    if mode == 3:
        print('Mode Null...')
    if mode == 4:
        print('Mode Null...')
    if mode == 5:
        print('Mode Null...')
    if mode == 6:
        print('System Mode...')
    
def button3press():
    print('Button 3 Pressed...')
    if mode == 1:
        print('Camera Mode...')
        B3()
    if mode == 2:
        print('Gallery Mode...')
    if mode == 3:
        print('Mode Null...')
    if mode == 4:
        print('Mode Null...')
    if mode == 5:
        print('Mode Null...')
    if mode == 6:
        print('System Mode...')
        os.system('shutdown -r now')
    
def button4press():
    print('Button 4 Pressed...')
    if mode == 1:
        print('Camera Mode...')
        B4()
    if mode == 2:
        print('Gallery Mode...')
        print('Printing Current Photo')
        printPhoto()
    if mode == 3:
        print('Mode Null...')
    if mode == 4:
        print('Mode Null...')
    if mode == 5:
        print('Mode Null...')
    if mode == 6:
        print('Shuting Down System')
        os.system('shutdown -h now')


def startup():
    led1.on()
    led2.on()
    led1.blink(interval, interval)
    global mode
    mode = 1
    sleep(3)
    led1.off()
    
def printPhoto(documentPath):
    print('Printing Document')
    os.system("lp -d " + printerName + " -o fit-to-page -o media=4x6 " + documentPath)


try:
    startup()
    print('Waiting For User Input...')
    # button1.when_pressed = go_blink
    button1.when_pressed = button1press
    button2.when_pressed = button2press
    button3.when_pressed = button3press
    button4.when_pressed = button4press
    Sel0.when_pressed = selector0
    Sel1.when_pressed = selector1
    Sel2.when_pressed = selector2
    Sel3.when_pressed = selector3
    Sel4.when_pressed = selector4
    Sel5.when_pressed = selector5

    pause()

except KeyboardInterrupt:
    pass

finally:
    led1.close()
    led2.close()
