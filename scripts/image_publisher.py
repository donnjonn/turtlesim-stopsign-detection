#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import sys
 
rospy.init_node('image_publisher', anonymous=True)
bridge = CvBridge()
pub = rospy.Publisher('camera/image',Image,queue_size=1)
cap = cv2.VideoCapture(0)
 
rate = rospy.Rate(10)
while not rospy.is_shutdown():
    # Capture frame-by-frame
    ret, frame = cap.read()
    #cv2.imshow('frame', frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
       # break 
    # Check if grabbed frame is actually full with some content
    if ret:
        try:
            # Publish image
            pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
            print(e)

    rate.sleep()
