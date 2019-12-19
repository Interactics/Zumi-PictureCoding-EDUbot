#!/usr/bin/env python



import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from Line_detect_ros.msg import center
import cv2  
import numpy as np


def LineDetection():
    rospy.init_node('LineDetect', anonymous=False)
    rospy.Subscriber("/video", Image, callback)
    rospy.spin()


#not use
def grayscale(img):  
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#not use
def canny(img, low_threshold, high_threshold):  
    return cv2.Canny(img, low_threshold, high_threshold)

#not use
def gaussian_blur(img, kernel_size): 
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  


    mask = np.zeros_like(img) 

    if len(img.shape) > 2: 
        color = color3
    else:  
        color = color1


    cv2.fillPoly(mask, vertices, color)


    ROI_image = cv2.bitwise_and(img, mask)

    return ROI_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2): 
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10): 
    cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): 
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    # line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    # draw_lines(line_img, lines)

    return lines


def weighted_img(img, initial_img, a=1, b=1., r=0.):  
    return cv2.addWeighted(initial_img, a, img, b, r)


# 10 Frame overlap


def get_fitline(img, f_lines): 
    lines = np.squeeze(f_lines)
    lines = lines.reshape(lines.shape[0] * 2, 2)
    rows, cols = img.shape[:2]
    output = cv2.fitLine(lines, cv2.DIST_L2, 0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0] - 1) - y) / vy * vx + x), img.shape[0] - 1
    x2, y2 = int(((img.shape[0] / 2 + 100) - y) / vy * vx + x), int(img.shape[0] / 2 + 100)

    result = [x1, y1, x2, y2]
    return result


# image = cv2.imread('image.png')  

def callback(data):
    rospy.loginfo('Incomming Video')

    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("window", image)
    cv2.waitKey(3)

    height, width = image.shape[:2]  

    # gray_img = grayscale(image) 
    img_to_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # blur_img = gaussian_blur(gray_img, 3) 
    img_to_gauss = cv2.GaussianBlur(img_to_gray, (3, 3), 0)

    # canny_img = canny(blur_img, 70, 210)  
    img_to_canny = cv2.Canny(img_to_gauss, 70, 210)

    #ROI

    vertices = np.array(
        [[(50, height), (width * 1 / 5, height / 2 + 60), (width * 4 / 5, height / 2 + 60), (width - 50, height)]],
        dtype=np.int32)

    ROI_img = region_of_interest(img_to_canny, vertices)


    line_arr = hough_lines(ROI_img, 1, 1 * np.pi / 180, 30, 10, 20)  
    line_arr = np.squeeze(line_arr)

    if line_arr.shape[0] > 0 :


        slope_degree = (np.arctan2(line_arr[:, 1] - line_arr[:, 3], line_arr[:, 0] - line_arr[:, 2]) * 180) / np.pi


        line_arr = line_arr[np.abs(slope_degree) < 160]
        slope_degree = slope_degree[np.abs(slope_degree) < 160]

        line_arr = line_arr[np.abs(slope_degree) > 95]
        slope_degree = slope_degree[np.abs(slope_degree) > 95]

        L_lines, R_lines = line_arr[(slope_degree > 0), :], line_arr[(slope_degree < 0), :]
        temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        L_lines, R_lines = L_lines[:, None], R_lines[:, None]

        left_fit_line = get_fitline(image, L_lines)
        right_fit_line = get_fitline(image, R_lines)

        draw_fit_line(temp, left_fit_line)
        draw_fit_line(temp, right_fit_line)

        #Center of Line

        Center_of_Line_X = (left_fit_line[0] + left_fit_line[2] + right_fit_line[0] + right_fit_line[2]) // 4
        Center_of_Line_Y = (left_fit_line[1] + left_fit_line[3] + right_fit_line[1] + right_fit_line[3]) // 4

        result = weighted_img(temp, image)  
        cv2.imshow('result', result)  
        cv2.waitKey(3)



# break

#image.realse()
#cv2.destroyAllWindows()

if __name__ == '__main__':
    LineDetection()
