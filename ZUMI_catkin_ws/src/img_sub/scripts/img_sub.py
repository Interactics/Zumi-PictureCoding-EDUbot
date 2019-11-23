#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def incomming_node() :
    rospy.init_node('video_sub', anonymous=False)
    rospy.Subscriber("/video", Image, callback)
    rospy.spin()

def callback(data) :
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data,"bgr8")
    cv2.imshow("window", cv_image)
    cv2.waitKey(3)

    rospy.loginfo('Video is sub')

if __name__ == '__main__' :
    incomming_node()
