
import time
from std_msgs.msg import *
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

def main():
    stream = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN    
    
    while True:
        grabbed, frame = stream.read()        
        height, width, channels = frame.shape

        cropped = frame[0:height, 0:width]
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

        maximum = max(countAzul, countVioleta, countRojo, countAmarillo)            
        if maximum == countAzul:
            color = "Azul"
        elif maximum == countVioleta:
            color = "Violeta"
        elif maximum == countAmarillo:
            color = "Amarillo"
        elif maximum == countRojo:
            color = "rojo"         

        cv2.putText(resized_cropped, "{0}".format(countAzul), (50, 50), font, 2, (255, 0, 0), 3)
        """cv2.putText(resized_cropped, "{0}".format(countAmarillo), (200, 50), font, 2, (0, 255, 0), 3)
        cv2.putText(resized_cropped, "{0}".format(countRojo), (350, 50), font, 2, (0, 0, 255), 3)"""

        cv2.imshow('my webcam', resized_cropped)

        cv2.imshow("Camara", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    stream.release()
    cv2.destroyAllWindows()

main()