#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import String

flag=False
codelist = []

rospy.init_node("pic_code_collector", anonymous=False)

pub = rospy.Publisher('/zumi/piccode_Coding', String, queue_size=1)
rate = rospy.Rate(10)

def picturecoding() : 
    rospy.Subscriber("/zumi/piccode_data", String, callback, queue_size =1)
    rospy.spin()

def callback(data) :
    global flag,codelist

    if data.data == 'START' : 
        flag = True
    
    elif data.data == 'DONE' : 
        codelist.append(data.data)
        flag = False

# 0: BACKWARD 1: DONE 2: TURN_RIGHT 3: FALSE_LEFT 4: FORWARD 5: FALSE_RIGHT
# 6: MUSIC 7: NOPE 8: START 9: TURN_LEFT

        for Code in codelist :
            pub.publish(Code)
            print Code
            rospy.sleep(3)

            #publish Code Data

        codelist = []

    if data.data == 'check' :
        for Code in codelist :
            print Code


    if flag == True and data.data != 'START' and data.data != 'NOPE' :
        codelist.append(data.data)

    elif flag ==True and data.data == 'NOPE' :
        codelist.pop()

    rospy.sleep(3)


if __name__ == "__main__" :
    picturecoding()
    