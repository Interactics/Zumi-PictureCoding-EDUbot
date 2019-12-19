#!/usr/bin/env python
    
import rospy
import smbus
import time
from geometry_msgs.msg import Point
from std_msgs.msg import String

STACK = []
CodeFlag = 0
x = 80

#i2c = I2CComm() 

def MoveZumi():
    global CodeFlag

    rospy.init_node('Move_Zumi', anonymous=False)
   
    rospy.Subscriber("/zumi/Pose", Point, Move)
    rospy.Subscriber("/zumi/piccode_Coding", String, Store, queue_size =10)
       



    rospy.spin()

class I2CComm(object):
    I2C_BUS_NUM = 1 

    def __init__(self):
        self.master = smbus.SMBus(self.I2C_BUS_NUM)
        self.slave_addr_list = [0x04,0x05]


    def test(self):
        me = self.master
        try :
            me.write_byte(4, 1)
        except IOError :
            time.sleep(1)
            print 1



    def run(self):
        me = self.master
   
        on_off = trans_spd(40,40) 
       
        for addr in self.slave_addr_list :
            try:
                me.write_byte(addr, int(on_off))
            except IOError:
                 pass
        time.sleep(1)


    def left(self):
        me = self.master
        on_off = trans_spd(-40,40)

        for addr in self.slave_addr_list :
            try:
                me.write_byte(addr, int(on_off))
            except IOError:
                pass
                time.sleep(1)

    def right(self):
        me = self.master
        on_off =trans_spd(40,-40)

        for addr in self.slave_addr_list :
            try:
                me.write_byte(addr, int(on_off))
            except IOError:
                pass
                time.sleep(1)

    def go(self):
        me = self.master
        on_off = trans_spd(60,40) 

        for addr in self.slave_addr_list :
            try:
                me.write_byte(addr, int(on_off))
            except IOError:
                pass
                time.sleep(1)

    def back(self):
        me = self.master
        on_off = trans_spd(-40,-40)

        for addr in self.slave_addr_list :
            try:
                me.write_byte(addr, int(on_off))
            except IOError:
                pass
                time.sleep(1)

    def stop(self):
        me = self.master
        on_off = trans_spd(0,0)

        for addr in self.slave_addr_list :
            try:
                me.write_byte(addr, int(on_off))
            except IOError:
                pass
                time.sleep(1)
                        

    def driving(self):
        me = self.master
        
        if x > 85 :
            LeftMotr =  40
            RightMotr = 50
        elif x< 75 :
            LeftMotr = 50
            RightMotr = 40

        else : 
            LeftMotr = 40
            RightMotr = 40

        on_off = trans_spd(LeftMotr, RightMotr)

        for addr in self.slave_addr_list :
            try:
                me.write_byte(addr,int(on_off))
            except IOError:
                pass
                time.sleep(1)

i2c = I2CComm()        
def Store(data) :
    global STACK, CodeFlag
    
    STACK.append(data.data)
    rospy.sleep(1)
    print data.data
    print STACK
    if data.data == 'DONE' :
        CodeFlag = 1
        print CodeFlag

    if CodeFlag == 1 : 
        PictureCoding()
       
def trans_spd(left, right) :

    if left > 0 : 
        if left < 20 :
            left = 10

        elif left >50 :
            left = 40
       
        else : 
            left = left - 10

        left_mtr = (left + 50)
    
    elif left < 0 :
        if left > -20 :
            left = -10
        elif left < -50 :
            left = -40
        else :
            left = left + 10 
        left_mtr = 50 + left
        
    else :
        left_mtr = 50


    if right > 0 :
        if right < 20 :
            right = 10
        elif right >50 :
            right = 40
        else : 
            right = right - 10
 
        right_mtr = (right + 50)//10 

    elif right < 0 :
        if right > -20 :
            right = -10
        elif right < -50 :
            right = -40
        else :
            right = right + 10

        right_mtr = (50 + right)//10

    else :
        right_mtr = 5


    velocity = left_mtr + right_mtr
    
    return velocity


def PictureCoding() :
    global STACK, CodeFlag

    for argm in STACK : 
        if argm  == 'BACKWARD' :
            i2c.back()
            rospy.sleep(3)
            print 'back motion'
            i2c.stop()

        elif argm == "DONE" :
            CodeFlag = 0
            STACK =[]
            print 'finish'

        elif argm  == "TURN_RIGHT" :
            i2c.right()
# rospy.sleep(3)
            i2c.stop()
            print 'right Turning'

        elif argm == "FORWARD" :
            i2c.go()
            rospy.sleep(3)
            i2c.stop()
            print 'go Forward'


        elif argm == "TURN_LEFT" :
            i2c.left()
# rospy.sleep(3)
            i2c.stop()
            print 'Turn left motion'
        else :
            pass 
       
 
def main():
#    i2c = I2CComm() 
#    i2c.right()
#    i2c.left()
    # rospy.sleep(0.5)
#    i2c.right()
    i2c.go()
#    i2c.back()
    i2c.stop() 

def Move(data):
    global x 


#flag

#   if flag = 'go' :

#    eif flag = '


#    if flag =
   #i2c = I2CComm()
    
    x = int(data.x)
    y = int(data.y)

    print 'x', x
    print 'y', y
    if y == -1 :
        print 'y is -1'
        i2c.stop()
    else :
        print 'y is not -1'
        i2c.driving()



if __name__ == "__main__" :
#    global CodeFlag

    main()
    MoveZumi()
#    if CodeFlag == 1 :
#        PictureCoding()

#END 
