#!/usr/bin/env python

import rospy
import cv2 as cv
from datetime import datetime
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

cv_image = 0 
sudan = 0
lugol = 0
biuret = 0

aftersudan = 0
afterlugol = 0
afterbiuret = 0

def callback(data):
    global sudan,lugol,biuret,afterbiuret,aftersudan,afterlugol
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    now = datetime.now()
    cv.imshow("Image window", cv_image)
    a = cv.waitKey(1)
    if a &0xFF == ord("a"):
        cv.imwrite("/home/arihc/Web_Interface/static/img/sudan"+str(sudan)+".png",cv_image)
        sudan+=1
    if a &0xFF == ord("b"):
        cv.imwrite("/home/arihc/Web_Interface/static/img/lugol"+str(lugol)+".png",cv_image)
        lugol+=1
    elif a &0xFF == ord("c"):
        cv.imwrite("/home/arihc/Web_Interface/static/img/biuret"+str(biuret)+".png",cv_image)
        biuret+=1
    
    # AFTER
    elif a &0xFF == ord("d"):
        aftersudan
        cv.imwrite("/home/arihc/Web_Interface/static/img/aftersudan"+str(aftersudan)+".png",cv_image)
        aftersudan+=1
    elif a &0xFF == ord("e"):
        cv.imwrite("/home/arihc/Web_Interface/static/img/afterlugol"+str(afterlugol)+".png",cv_image)
        afterlugol+=1
    elif a &0xFF == ord("f"):
        cv.imwrite("/home/arihc/Web_Interface/static/img/afterbiuret"+str(afterbiuret)+".png",cv_image)
        afterbiuret+=1
        
rospy.init_node('lab_photo_taker')
bridge = CvBridge()
image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,callback)


rate = rospy.Rate(10)

while not rospy.is_shutdown():
	try:
		rate.sleep()

	except rospy.ROSInterruptException:
		rospy.logerr("ROS Interrupt Exception, done by User!")
	except rospy.ROSTimeMovedBackwardsException:
		rospy.logerr("ROS Time Backwards! Just ignore it!")