import time
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

def main():    

    stream = cv2.VideoCapture(2)
    font = cv2.FONT_HERSHEY_PLAIN

    while True:
        grabbed, frame = stream.read()
        if not grabbed:
            break
        decodedObjects = pyzbar.decode(frame)

        for obj in decodedObjects:
            num = int(obj.data)   
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow('my webcam', frame)
        

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    stream.release()
    cv2.destroyAllWindows()

main()