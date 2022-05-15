
import time
from std_msgs.msg import *
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import matplotlib.pyplot as plt

def buildHistogram(color):
    histogram = [0] * 256
    for row in color:
        for cell in row:
            histogram[cell]+=1
    return histogram

def main():
    stream = cv2.VideoCapture(0)
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
        height, width, channels = frame.shape

        cropped = frame[0:height, 0:width]
        resized_cropped = cv2.resize(cropped, (width, height))

        B, G, R = cv2.split(resized_cropped)
        histoB = buildHistogram(B)
        histoG = buildHistogram(G)
        histoR = buildHistogram(R)
        """plt.hist(histoB)
        plt.show()"""
        cv2.putText(resized_cropped, "{0}".format(int(np.mean(R))), (50, 50), font, 2, (255, 0, 0), 3)
        cv2.putText(resized_cropped, "{0}".format(int(np.mean(G))), (200, 50), font, 2, (0, 255, 0), 3)
        cv2.putText(resized_cropped, "{0}".format(int(np.mean(B))), (350, 50), font, 2, (0, 0, 255), 3)

        cv2.imshow('my webcam', resized_cropped)

        cv2.imshow("Camara", frame)

        key = cv2.waitKey(1) & 0xFF
        break
        if key == ord("q"):
            break
    stream.release()
    cv2.destroyAllWindows()

main()