#!/usr/bin/python3

import os
import cv2
import time
import imutils
import numpy as np
from signal import pause
from time import sleep
from gpiozero import LED, Button

blink_on = False
interval = 0.1

button1 = Button(5) # No Filter Button
button2 = Button(6) # Greyscale Button
button3 = Button(13) # Sepia Button
button4 = Button(26) # Shutdown Button
led1 = LED(23) # Ready Status LED - Green
led2 = LED(24) # Processing Status LED - Orange


def fileNameCheck():
    
    i = 0
    while os.path.exists(f"/home/pi/image_{i}.jpg"):
        i += 1
    
    fileName = f"/home/pi/image_{i}.jpg"
    return fileName

def sepia(src_image):
    gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32)/255
    #solid color
    sepia = np.ones(src_image.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R
    #hadamard
    sepia[:,:,0] *= normalized_gray #B
    sepia[:,:,1] *= normalized_gray #G
    sepia[:,:,2] *= normalized_gray #R
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
    #Monochrome Filter To Photo
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

def B1(): # No Filter
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
    print('Awaiting User Input...')
    
    # Set Status LED's Back to Ready Status
    led2.on()
    led1.off()
    
def B2(): # Greyscale Filter
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
    #Monochrome Filter To Photo
    image = cv2.imread(outputFile)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    cv2.imwrite(outputFile, gray) 
    print('Done Applying Greyscale Filter, Photo Is Located At: ' + outputFile)
    print('Awaiting User Input...')
    
    # Set Status LED's Back To Ready Status
    led2.on()
    led1.off()
    
def B3(): # Sepia Filter
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
    print('Awaiting User Input...')

    # Setting LED'S to Ready Mode
    led2.on()
    led1.off()

def B4(): # Soft Shutdown Button
    print('Button 4 Pressed...')
    led1.on()
    led2.blink(interval, interval)
    sleep(2)
    led2.on()
    led1.off()
    
def startup():
    led1.on()
    led2.on()
    led1.blink(interval, interval)
    sleep(3)
    led1.off()
    

try:
    startup()
    print('Waiting For User Input...')
    # button1.when_pressed = go_blink
    button1.when_pressed = B1
    button2.when_pressed = B2
    button3.when_pressed = B3
    button4.when_pressed = B4
    pause()

except KeyboardInterrupt:
    pass

finally:
    led1.close()
    led2.close()