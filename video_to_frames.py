import cv2
import numpy as np

vidcap = cv2.VideoCapture('resources/eye.mp4')
success,image = vidcap.read()
count = 0

previous_frame = 0
current_frame = 0


def detect_eye(image):
    eye_detector = cv2.CascadeClassifier('/home/srujan/PycharmProjects/AR_project/venv/lib/python3.5/site-packages/cv2/data/haarcascade_eye.xml')
    eyes = eye_detector.detectMultiScale(image)
    current_bounding_box = eyes[0]
    # p1 = (int(current_bounding_box[0]), int(current_bounding_box[1]))
    # p2 = (int(current_bounding_box[0] + current_bounding_box[2]), int(current_bounding_box[1] + current_bounding_box[3]))
    return current_bounding_box


def good_key_points(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)

x = 0
y = 0
w = 0
h = 0
p1 = 0
p2 = 0
p1w = 0
p2h = 0

success = True
while success:
    success,image = vidcap.read()

    if count == 0:
        eyes = detect_eye(image)

        x = eyes[0]
        y = eyes[1]
        w = eyes[2]
        h = eyes[3]
    else:
        x = p1
        y = p2
        w = p1w
        h = p2h

    p1 = x
    p2 = y

    p1w = w
    p2h = h

    roi = image[p2:p2+p2h, p1:p1+p1w]

    gray_eye = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # gray_eye = roi

    ## white mask
    ret, mask3 = cv2.threshold(gray_eye, 150, 255, cv2.THRESH_BINARY)
    # ret, mask3 = cv2.threshold(gray_eye, 175, 255, cv2.THRESH_BINARY)

    ## gray mask
    ret, mask4 = cv2.threshold(gray_eye, 0, 10, cv2.THRESH_BINARY)

    mask5 = cv2.bitwise_or(mask3,mask4)

    # gray_eye = roi


    # x, threshold_image = cv2.threshold(gray_eye,25,255,cv2.THRESH_BINARY_INV)
    # equa_img = cv2.equalizeHist(gray_eye)
    # edges = cv2.Canny(equa_img,100,150,7 )
    #
    # corner = cv2.cornerHarris(equa_img,2,3,0.04)

    # gray_eye[:,:,0] = 0
    #
    # lower_white = np.array([255,255,255])
    # upper_white = np.array([0,0,0])
    # mask_1 = cv2.inRange(gray_eye,lower_white,upper_white)
    # lower_gray = np.array([75,75,75])
    # upper_gray = np.array([0,0,0])
    # mask_2 = cv2.inRange(gray_eye,lower_gray,upper_gray)
    # mask = cv2.bitwise_or(mask_1,mask_2)

    eye_masked = cv2.bitwise_not(roi,roi, mask = mask5)
    # eye_masked1 = cv2.bitwise_not(eye_masked,eye_masked, mask = mask4)


    # equa_img = cv2.equalizeHist(gray_eye[:,:,2])

    # cv2.imshow('press', equa_img)
    cv2.imshow('press', eye_masked)

    # cv2.imshow('thres', corner)
    cv2.waitKey(0)

    if cv2.waitKey(25) & 0xff == 27:  # To get the correct frame rate
        cv2.destroyAllWindows()
        break




    count += 1
