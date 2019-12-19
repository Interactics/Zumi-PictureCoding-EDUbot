#!/usr/bin/env python
import rospy
import sys
import os
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image



def start_node():
    os.system('sudo modprobe bcm2835-v4l2')   
    rospy.init_node('video_pub')
    rospy.loginfo('video_pub node started')
    
    #img = cv2.imread(filename)

    ####open Camera and Camera setting
    img = cv2.VideoCapture(0)
    img.set(3,640/4)
    img.set(4,480/4)
#    img = cv2.flip(img,0)
#    img = cv2.flip(img,1)
    
    #cv2.imshow("image",img)
    #cv2.waitKey(2000)
    
    bridge = CvBridge()
    #imgMsg = bridge.cv2_to_imgmsg(img, "bgr8")

    pub = rospy.Publisher('video', Image, queue_size =1)
    while not rospy.is_shutdown():

        ret, frame = img.read()
        if not ret :
            print('Not Found Camera')
            break


        #cv2.imshow('video', frame)
        imgMsg = bridge.cv2_to_imgmsg(frame,"bgr8")
        pub.publish(imgMsg)
             
#  if cv2.waitKey(2)&0xFF == 27:
#            break
        
        rospy.Rate(5).sleep()


    img.release()
    cv2.destroyAllWindows()

if __name__ == '__main__' :
    try :
        start_node()
    except rospy.ROSInterruptException:
        pass


