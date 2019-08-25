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
CLOSE_WIDTH = 50 #how close should the stop sign be before being detected (= minimum width in pixels of the stop sign before being detected)
LINEAR_VEL = 4 #velocity along the turtle's x-axis
ANGULAR_VEL = 2 #angular velocity around turtles z-axis (radians/sec)
SCALE_FACTOR = 1.1 #how fast will sliding window increase in size (lower = better performance but lower speed)
MIN_NEIGHBOURS = 10 #how many neighbours before a positive match is genrated
close = False
"""haar classifier from https://github.com/markgaynor/stopsigns.git"""
"""lbp classifier from https://github.com/ojcodes/StopSignDetection.git"""
def detect_stop(classifier, frame):
    #Load the classifier and read the image.
    classifier = cv2.CascadeClassifier(classifier)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect any stop signs in the image using the classifier at various scales.
    stop_signs = classifier.detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBOURS)
    return stop_signs

def callback(msg):
    close = False
    try:
        frame = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)
    if(args["classifier"]=="lbp"):
        stop_signs = detect_stop("stopsign_classifier_lbp.xml", frame)
    else:
        stop_signs = detect_stop("stopsign_classifier_haar.xml", frame) 
    vel_msg = Twist()
    for (x,y,w,h) in stop_signs:
        #if stop sign close enough (>CLOSE_WIDTH) to camera "close" variable to true
        if w > CLOSE_WIDTH:
            close = True
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        quit()
    if len(stop_signs) > 0 and close == True:
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
    else:
        vel_msg.linear.x = LINEAR_VEL
        vel_msg.angular.z = ANGULAR_VEL
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
       


