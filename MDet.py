#!usr/bin/env python

import datetime
import sys
import cv2
# A PROGRAM IN PYTHON TO DETECT MOVEMENT AND SEND NOTIFICATION WHENE A MOVEMENT IS DETECTED


# create VIDEOCAPTURE OBJECT
cap = cv2.VideoCapture(0) # åpner default Kamera, gi 0 som argument ellers kan man gi URL av en video
# Stream av en IP Kamera.

# Backgroung substractor, bruker MOG2 for å detektere skygge
substractor = cv2.createBackgroundSubtractorMOG2()



# implementing functionality in a given time, it can be outside working hours in corridor 
now =datetime.datetime.now().time()
workingtime=now>=datetime.time(8,0) and now<=datetime.time(16,0)

if workingtime:
    #notify( UI)
    print("IT IS A SURVEILLANCE TIME : " , now)
    print("SURVEILLANCE ACTIVATED ...")
    
  

if not workingtime:  # outside working time/ sys.exit()
    print("NOT WORKING TIME, EXITING ...")
    sys.exit()


while workingtime: # justert til working time
    # can be opened in (UI)

    # les Frame fra Kamera
    ret, frame = cap.read() # ret er boolean her som returnerer True hvis frame er tilstedet

    
    foreGroundMask = substractor.apply(frame) # fgmask binary image(mask) where white points are foreground and black points are background

    # foreGroundMask countours
    # RETR_EXTERNAL retrieve just external contours
    contours, hierarchy = cv2.findContours(foreGroundMask, cv2.RETR_EXTERNAL, cv2.CALIB_HAND_EYE_ANDREFF)

    # Draw contours on the original frame
    for c in contours:
        if cv2.contourArea(c) > 600: # kalibrer sensivitet
            (x, y, w, h) = cv2.boundingRect(c) #top left corner(x,y) , width ang height of the bounding rectangle ogf the contour c
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)# draw a rectangle on the frame starting from x,y -> bottom right corner -> use a color , and thickness of the line.
            print("movement detected") # notify() a system (implement )

    # Show the original frame with contours drawn on it
    cv2.imshow('frame', frame)

    
    if cv2.waitKey(1) == ord(chr(27)): # exit using esc key
        sys.exit()

cap.release()


cv2.destroyAllWindows()    




