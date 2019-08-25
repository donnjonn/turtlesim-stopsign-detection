#!/usr/bin/env python

import numpy as np
import imutils
import argparse
import cv2
import rospy
import sys
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
framecount = 0
close = False
"""haar classifier from https://github.com/markgaynor/stopsigns.git"""
"""lbp classifier from https://github.com/ojcodes/StopSignDetection.git"""
def detect_stop(classifier, img, example=False):
    #Load the classifier and read the image.
    classifier = cv2.CascadeClassifier(classifier)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect any stop signs in the image using the classifier at various scales.
    stop_signs = classifier.detectMultiScale(gray, 1.02, 10)
    return stop_signs

def callback(msg):
    close = False
    try:
        frame = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)
    #if framecount%10 == 0:
    if(args["classifier"]=="lbp"):
        stop_signs = detect_stop("stopsign_classifier_lbp.xml", frame, True)
    else:
        stop_signs = detect_stop("stopsign_classifier_haar.xml", frame, True)
    #stop_signs = detect_haar("stopsign_classifier.xml", frame, True)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()   
    vel_msg = Twist()
    for (x,y,w,h) in stop_signs:
        #if stop sign close to camera (>1/2 of resolution width) set "close" variable to true)
        if w > 250:
            close = True
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        quit()
    if len(stop_signs) > 0 and close == True:
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
    else:
        vel_msg.linear.x = 4
        vel_msg.angular.z = 2 
    vel_msg.angular.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.y = 0
    pub.publish(vel_msg)

rospy.init_node('stop_sign_detection', anonymous=True)
bridge = CvBridge()
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--classifier", required=True, choices=["haar", "lbp"], help="which classifier?(haar(more accurate) or lbp(faster))")
args = vars(ap.parse_args())
pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=1)
sub = rospy.Subscriber('camera/image', Image, callback)

rospy.spin()        
       


