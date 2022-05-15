#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import *
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

pubColor = rospy.Publisher('/lab_color',String,queue_size = 10)
pubTest = rospy.Publisher('/lab_test',Int64,queue_size = 10)

def main():
    rospy.init_node("lab_detect")
    rate = rospy.Rate(2)

    stream = cv2.VideoCapture(2)
    font = cv2.FONT_HERSHEY_PLAIN
    #PROTEINA
    azulBajo = np.array([100, 100, 20], np.uint8)
    azulAlto = np.array([125, 255, 255], np.uint8)
    violetaBajo = np.array([130, 100, 20], np.uint8)
    violetaAlto = np.array([145, 255, 255], np.uint8)
    
    amarilloBajo = np.array([15, 100, 20], np.uint8)
    amarilloAlto = np.array([45, 255, 255], np.uint8)
    redBajo1 = np.array([0, 100, 20], np.uint8)
    redAlto1 = np.array([5, 255, 255], np.uint8)
    redBajo2 = np.array([175, 100, 20], np.uint8)
    redAlto2 = np.array([179, 255, 255], np.uint8)
    while True:
        grabbed, frame = stream.read()
        if not grabbed:
            break
        decodedObjects = pyzbar.decode(frame)

        for obj in decodedObjects:
            num = int(obj.data)
            pubTest.publish(num)
            print(num)
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            xc = int(x+(w/2))
            yc = int(y+(h/2))
            #cv2.putText(frame, "{0}  {1}  {2}  {3}".format(x,y,w,h), (50, 50), font, 2, (255, 0, 0), 3)
            #cv2.rectangle(frame, (xc, yc), (xc+2, yc+2), (0, 255, 0), 2)
            # cv2.circle(frame,(xc,yc),7,(0,255,0),-1)
            #try:
            height, width, channels = frame.shape
            #Alturas
            minX = yc
            maxX = yc+20
            #Widths
            minY = xc
            maxY = xc+20
            cropped = frame[minX:maxX, minY:maxY]
            resized_cropped = cv2.resize(cropped, (width, height))

            frameHSV = cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2HSV)
            maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
            maskVioleta = cv2.inRange(frameHSV, violetaBajo, violetaAlto)
            maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
            maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
            maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
            maskRed = cv2.add(maskRed1, maskRed2)
            
            countAmarillo = cv2.countNonZero(maskAmarillo)
            countAzul = cv2.countNonZero(maskAzul)
            countVioleta = cv2.countNonZero(maskVioleta)
            countRojo = cv2.countNonZero(maskRed1) + cv2.countNonZero(maskRed2) + cv2.countNonZero(maskRed)

            msg = String()            
            color = "No encontrado"

            maximum = max(countAzul, countVioleta, countRojo, countAmarillo)            
            if maximum == countAzul:
                color = "Azul"
            elif maximum == countVioleta:
                color = "Violeta"
            elif maximum == countAmarillo:
                color = "Amarillo"
            elif maximum == countRojo:
                color = "rojo"         
            print(color)
            msg.data = color                
            pubColor.publish(msg)

            cv2.putText(resized_cropped, "{0}".format(countAzul), (50, 50), font, 2, (255, 0, 0), 3)
            """cv2.putText(resized_cropped, "{0}".format(countAmarillo), (200, 50), font, 2, (0, 255, 0), 3)
            cv2.putText(resized_cropped, "{0}".format(countRojo), (350, 50), font, 2, (0, 0, 255), 3)"""

            cv2.imshow('my webcam', resized_cropped)

            """except:
                print("error")"""
        cv2.imshow("Camara", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    stream.release()
    cv2.destroyAllWindows()

main()