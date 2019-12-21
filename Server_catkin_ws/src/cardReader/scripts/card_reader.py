#!/usr/bin/env python

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD,RMSprop,adam
from keras.utils import np_utils
from keras.models import load_model
from keras import backend as K
import numpy as np
import cv2
import time
# SKLEARN
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import json
import time
import matplotlib
from matplotlib import pyplot as plt
import threading
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image as ImageMsg
#matplotlib.use("TkAgg")
import tensorflow as tf

graph = tf.get_default_graph()



prev_time = 0
if K.backend() == 'tensorflow':
    import tensorflow
    #K.set_image_dim_ordering('tf')
else:
    import theano
    #K.set_image_dim_ordering('th')
K.set_image_dim_ordering('th')
   
   
import numpy as np
#import matplotlib.pyplot as plt
import os
from PIL import Image



rospy.init_node("piccode_data", anonymous=False)
pub = rospy.Publisher('/zumi/piccode_data', String, queue_size=1)

def listner() :
    rospy.loginfo('Card_reader_online')

    rospy.Subscriber("/video", ImageMsg, detector, queue_size=1)
    rospy.spin()




# pub = rospy.Publisher('/zumi/piccode_data', String, queue_size=1)
# rate = rospy.Rate(10)


minValue = 70

jsonarray = {}
# input image dimensions
img_rows, img_cols = 50, 50
# maxWidth, maxHeight = img_rows, img_cols

# number of channels
# For grayscale use 1 value and for color images use 3 (R,G,B channels)
img_channels = 1

nb_classes = 10

# Total number of convolutional filters to use
nb_filters = 32
# Max pooling
nb_pool = 2
# Size of convolution kernel
nb_conv = 3

WeightFileName = []

output = ["BACKWARD", "DONE", "FALSE_LEFT", "FORWARD", "FALSE_RIGHT", "MUSIC", "NOPE", "START", "TURN_LEFT", "TURN_RIGHT"]


def modlistdir(path, pattern = None):
    listing = os.listdir(path)
    retlist = []
    for name in listing:
        #This check is to ignore any hidden files/folders
        if pattern == None:
            if name.startswith('.'):
                continue
            else:
                retlist.append(name)
        elif name.endswith(pattern):
            retlist.append(name)
            
    return retlist

def loadCNN(bTraining = False):
    global get_output
    model = Sequential()
    
    
    model.add(Conv2D(nb_filters, (nb_conv, nb_conv),
                        padding='valid',
                        input_shape=(img_channels, img_rows, img_cols)))

    convout1 = Activation('relu')
    model.add(convout1)
    model.add(Conv2D(nb_filters, (nb_conv, nb_conv)))
    convout2 = Activation('relu')
    model.add(convout2)
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    
    #sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    
    # Model summary
    #model.summary()

    # Model conig details
    #model.get_config()
    
    if not bTraining :
        
         WeightFileName = modlistdir('.','.hdf5')
         if len(WeightFileName) == 0:
            print('Error: No pretrained weight file found. Please either train the model or download one from the https://github.com/asingh33/CNNGestureRecognizer')
            return 0
         else:
             print('Found these weight files - {}'.format(WeightFileName))
         #Load pretrained weights
         w = int(input("Which weight file to load (enter the INDEX of it, which starts from 0): "))
         #w = int(0)
         fname = WeightFileName[int(w)]
         print("loading ", fname)
         model.load_weights(fname)

         # refer the last layer here
         layer = model.layers[-1]
         get_output = K.function([model.layers[0].input, K.learning_phase()], [layer.output,])
   
    
    return model



##### added


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def detector(data):
    global prev_time
    num_pic = 0
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    frame = cv2.flip(frame, 1)
    frame = cv2.flip(frame, 0)
    
    cv2.imshow("test", frame)
    cv2.waitKey(3)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 40, 200)
    contour, hierarcy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour = sorted(contour, key=cv2.contourArea, reverse=True)[:5]

    for c in contour:
        ## contour length
        peri = cv2.arcLength(c, True)
        area_size = cv2.contourArea(c)
        # size 10,000 ~ 100,000

        approx = cv2.approxPolyDP(c, peri * 0.02, True)
        screenCnt = []

        if len(approx) == 4:
            contourSize = cv2.contourArea(approx)
            camSize = frame.shape[0] * frame.shape[1]
            ratio = contourSize / frame.shape[1]

            if ratio > 10 and contourSize > 5000/16:
                screenCnt = approx
                #print ratio

            break

    if len(screenCnt) == 0:
        pass 
#        cv2.imshow("WebCam", frame)
        #cv2.imshow("edged", edged)

    else:
        cv2.drawContours(frame, screenCnt, -1, (0, 255, 0), 2)
        cv2.imshow("WebCam", frame)

        rect = order_points(screenCnt.reshape(4, 2))
        (topLeft, topRight, bottomLeft, bottomRight) = rect

        maxWidth = 50
        maxHeight = 50

        dst = np.float32([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]])

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))
        warp_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(warp_gray,(3,3),2)

        th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
        _, res = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #blur = cv2.GaussianBlur(gray,(5,5),2)
        cv2.imshow("Scanned", res)

        ## predict

        img = res
        img = np.array(img).flatten()
        img = img.reshape(img_channels, img_rows, img_cols)
        img = img.astype('float32')
        img = img / 255
        img = img.reshape(1, img_channels, img_rows, img_cols)

        #model = loadCNN()
###############################################################
	    #model.load_weights('/home/hy/catkin_ws2/src/cardReader/scripts/newWeight3.hdf5')
###############################################################
        with graph.as_default() :
            result = model.predict(img, steps=None)

        result = np.squeeze(result)
        #print(result)
        answer = result.argmax()

        cv2.waitKey(2)
        output[answer]

        Codedata = output[answer]
        if time.time() - prev_time > 5  :
            print ' The answer is', output[answer]

            publish = pub.publish(Codedata)
            prev_time = time.time()



if __name__ == "__main__":
	model = loadCNN()
	model.load_weights('/home/hy/catkin_ws2/src/cardReader/scripts/PCweight.hdf5')
	listner()

