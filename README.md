
# ZUMI PictureCoding EDUbot
---
[TeamAlphaZUMI]

한양대학교 ERICA 로봇공학과 박병우, 유호연, 이영준 

# 개요

---

한양대학교 ERICA 로봇공학과 로봇프로그래밍 수업의 일환으로 제작되었습니다. 

ZUMI는 Robolink사의 제품으로 이를 활용하여 ROS 패키지 제작 프로젝트를 진행하였습니다.

인공지능과 프로그래밍 교육이라는 기능을 확장하기 위해 Picture Coding을 활용하여 ZUMI의 사용 연령층을 확장시켰습니다.

Picture Coding은 그림 카드를 ZUMI에게 보여줌으로 로봇의 행동을 프로그래밍처럼 제어할 수 있는 기능입니다.

ZUMI는 각 그림 카드를 인식한 후 사용자에게 자신이 인식했다는 사실을 상호작용을 통하여 전달합니다.

# 하드웨어 개발환경

---

## ZUMI

---

- 아두이노 UNO
- RaspberryPi Zero W
- DC 모터 2개
- IR 6개
- LED 2개
- PiCam
- 디스플레이 Adafruit ssd1306

# 소프트웨어 개발환경

---

## Computer

---

- Ubuntu 18.04 Bionic
- ROS Melodic Morenia
- Arduino 1.8.10
- OpenCV 3.4.0
- Python 2.7
- Keras 2.2.4
- Theano 1.0.4
- Tensorflow 1.13.1

## ZUMI

---

- Raspbian Jessie (debian 8)
- ROS Kinetic Kame
- OpenCV 3.3.1
- python 2.7


# ROS 의존파일

---

- CV_bridge
- ros_serial

# 설치 및 사용 방법

---

## 설치

### Raspbian Jessie ROS 설치
http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi 지시사항을 따릅니다.

### 코드 사용 

github의 Repo를 복사하여 사용합니다.

    git clone https://github.com/yhyingit/Zumi-PictureCoding-EDUbot.git
    

    
    
## 사용법

ZUMI에서 카메라 데이터를 퍼블리시하는 패키지입니다.

    rosrun Zumicam Zumi_cam.py


PC에서 ZUMI로부터 영상 받은 후 차선 검출 후 차선의 중간 값을 퍼블리시하는 패키지입니다.

    rosrun zumi_line_detect Line_detection_ROS.py


PC에서 ZUMI가 받은 Picture Coding의 카드 모양을 뉴럴네트워크를 통해 모양을 추정한 뒤, 그 결과 값을 퍼블리시하는 패키지입니다.

    rosrun cardReader card_reader.py

- 12층(CNN 3층) 뉴럴네트워크 알고리즘을 활용해 PictureCoding 카드 3천장을 학습하여 10개의 클래스로 카드를 분류하였습니다.

    
PC에서 뉴럴네트워크로 처리한 카드의 정보 계속 구독한 후, 'DONE'(완료) 카드가 나올 때 까지 Stack 자료구조에 저장하는 패키지입니다.

    rosrun picCoding picCoding.py
    
    
ZUMI에서 코딩 카드가 입력되면 해당 카드에 대한 정보를 표정으로 표현하는 패키지입니다.

    rosrun Zumi_face zumi_face.py
    
    
ZUMI에서 각 카드 정보에 따라 로봇을 구동하는 패키지입니다.

    rosrun Zumi_move zumi_move.py





# 기능

---

이 시스템은 PC와 ZUMI의 기종 통신으로 작동합니다.

### 1. PictureCoding

- Coding 카드를 ZUMI에게 보여줌으로 카드를 인식시킵니다.
- CNN 활용하여 PictureCoding 카드를 인식하는 알고리즘을 가집니다..
- '시작' 카드를 인식시켜 코딩 단계에 돌입하며 '끝' 카드로 코딩단계를 종료합니다.
- 코딩 단계에서 사용자와 ZUMI와 상호작용을 통해 카드 인식상태를 확인할 수 있습니다.

### 2. 자율 주행 기능

- ZUMI에 탑재된 PiCam을 활용하여 차선을 검출합니다.
- 검출된 차선을 인식하여 도로 주행합니다.
- PictureCoding에서 프로그래밍한 방식으로 맵에서 자율적으로 주행합니다.

### 3. ZUMI 표정 표현

- Adafruit SSD1306 디스플레이를 활용하여 ZUMI의 표정을 표현합니다.
- 인식된 카드의 모양을 디스플레이에 표현합니다.
- 인식된 카드 모양을 화면에 표현한 후 상황에 맞는 표정 및 움직임을 표현합니다.


[ZUMI디스플레이 표현](https://www.notion.so/50861e024bcd44c2af302d7f1b26876c)

[ZUMI 감정 표현](https://www.notion.so/98cd471a58834eaf897d699f9848e860)


### 4. GAZEBO MAP

- Gazebo map editor를 활용하여 제작되었습니다.
- 조합하여 맵을 확장할 수 있습니다.

### 5. ZUMI URDF -- 미완성

- 솔리드웍스를 사용하여 ZUMI를 구현합니다.
- 모델을 활용하여 GAZEBO 환경에서 시뮬레이션합니다.

### Card

- "좌로 이동", "우로 이동"은 ZUMI의 구조와 물리적 특징 상 이동 불가 하기 때문에 이와 같은 카드들을 인식하면 의문을 갖는 표정을 띄웁니다.
- "시작"카드를 보여주며 프로그래밍의 시작을 인식시킵니다.
- "직진"과 "후진"카드를 보여주어 인식이 되는 경우 맵의 처음 교차로부터 다음 교차로 까지 한 블럭을 이동합니다.
- "시계방향으로 90도 회전"과 "반시계방향으로 90도 회전" 카드는 ZUMI를 90도 만큼 회전시킵니다.
- "시작"카드는 프로그래밍이 시작한다는 것을 알려주는 카드 입니다.
- "끝"카드는 프로그래밍을 끝남을 알려주는 카드입니다.
- "아니"카드는 직전에 인식시킨 프로그래밍을 취소할 때 사용하는 카드입니다.
- "일반적 표정"은 ZUMI의 일반적인 표정을 나타냅니다.
- "웃는 표정"은 ZUMI가 정상적인 인식을 할 경우와 프로그램이 시작할 때 짓는 표정입니다.
- 그외 카드는 인식할 수 없는 카드입니다.



# Node


![주석 2019-12-21 153127](https://user-images.githubusercontent.com/56077549/71304219-142bb080-2407-11ea-9d4a-e2331560a07b.png)


## PC

- piccode_data : 이미지로부터 코딩 카드를 인식하는 노드입니다. 
- LineDetect : 차선을 인식한 후 차선의 중앙값을 퍼블리시 하는 노드입니다. 
- pic_code_collector: Picutre Coding의 카드 데이터를 인식한 후 처리된 코딩 카드를 저장하는 노드입니다. 
 데이터를 /zumi/piccode_Coding 토픽으로 퍼블리시합니다. 


## ZUMI

- video_pub : 영상정보인 /video 토픽을 퍼블리시 노드입니다.
- zumi_face : 디스플레이를 담당하는 노드입니다.
- Move_Zumi : 아두이노와 연결되어 모터 제어를 담당하는 노드입니다.





# Topic

- /video : ZUMI 카메라가 보내는 영상 이미지 토픽
- /zumi/Pose : 감지된 차선의 중앙값 
- /zumi/piccode_Coding : 저장된 카드 데이터를 모터 노드에 던지기 위해 만든 토픽
- /zumi/piccode_data : 카메라로부터 카드 이미지를 받아 처리 후 토픽으로 만들어진 최초의 카드 이미지 토픽


# 발생한 이슈

- 카드를 인식하는 패키지인 cardReader 패키지는 해당 디렉토리에서 rosrun을 실행해야합니다.
- 차선 인식 후 주행은 추후 계획입니다.



# 참고

Raspbian + ROS 설치 :[http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi]

ZUMI : [https://www.robolink.com/zumi/](https://www.robolink.com/zumi/)

PictureCoding 학습 CNN Model : [https://github.com/asingh33/CNNGestureRecognizer](https://github.com/asingh33/CNNGestureRecognizer)

LineDetection : [https://github.com/windowsub0406/SelfDrivingCarND](https://github.com/windowsub0406/SelfDrivingCarND)

