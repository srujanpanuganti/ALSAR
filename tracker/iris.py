import os
import numpy
import sys
import cv2
import time


video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Could not open video, camera isn't working")
    sys.exit()
else:
    print('camera working')

detector = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')


all_imgs = []
count = 0
while True:
    count +=1
    ok,frame = video.read()
    gray = frame

    cv2.imshow('frame', gray)
    cv2.waitKey(5)

    detected_face = detector.detectMultiScale(gray,1.3,5)
    # print(detected_face)
    if detected_face:

        cropped = gray[detected_face[0][1]:detected_face[0][1]+detected_face[0][3], detected_face[0][0]:detected_face[0][0] + detected_face[0][2]]
        # resized = cv2.resize(cropped, (200,200))

        all_imgs.append(cropped)
    time.sleep(0.1)
    else:
        continue
