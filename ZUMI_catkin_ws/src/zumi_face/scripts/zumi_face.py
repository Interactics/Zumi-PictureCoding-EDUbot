#!/usr/bin/env python

from screen import *
import rospy 
from std_msgs.msg import String

eye = Screen()

def callback(data):
    inform = data.data
    if inform == 'UP' : 
        eye.normalface()
        time.sleep(1)
        eye.upward()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
    elif inform == 'DOWN' :
        eye.normalface()
        time.sleep(1)
        eye.downward()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
    elif inform == 'LEFT' :
        eye.normalface()
        time.sleep(1)
        eye.leftward()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
    elif inform == 'RIGHT' :
        eye.normalface()
        time.sleep(1)
        eye.reward()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
    elif inform == 'CCW' :
        eye.normalface()
        time.sleep(1)
        eye.ccw()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()    
    elif inform == 'CW' :
        eye.normalface()
        time.sleep(1)
        eye.cw()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()    
    elif inform == 'START' :
        eye.normalface()
        time.sleep(1)
        eye.start()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
    elif inform == 'DONE' :
        eye.normalface()
        time.sleep(1)
        eye.theend()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
    elif inform == 'HEART' :
        eye.normalface()
        time.sleep(1)
        eye.heart()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
    elif inform == 'IDK' :
        eye.normalface()
        time.sleep(1)
        eye.idk()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()  
    elif inform == 'MUSIC' :
        eye.normalface()
        time.sleep(1)
        eye.music()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface() 
    elif inform == 'NOPE' :
        eye.normalface()
        time.sleep(1)
        eye.Nop()
        time.sleep(1)
        eye.smile()
        time.sleep(1)
        eye.normalface()
                     
def listener():
    rospy.init_node('zumi_face', anonymous = False)
    rospy.Subscriber("/zumi/piccode_data",String,callback)
    eye.normalface()
    rospy.spin()




if __name__ == '__main__' :
    listener()
 
