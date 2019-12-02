import cv2
import numpy as np
from scipy import stats

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



def free_from_outliers(data):

    z = np.abs(stats.zscore(data))

    z_x = z[:,0]
    z_y = z[:,1]

    out_x = np.argwhere(z_x> np.mean(z_x))
    out_y = np.argwhere(z_y> np.mean(z_y))

    # print('mean_zx', np.mean(z_x), 'mean_zy', np.mean(z_y))

    if out_x.size > out_y.size:
        data = np.delete(data, out_x, 0)

    elif out_y.size > out_x.size:
        data = np.delete(data, out_y, 0)

    else:
        data = np.delete(data, out_x, 0)


    return data





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
    hsv_image = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # gray_eye = roi

    # ## white mask
    # ret, mask3 = cv2.threshold(gray_eye, 175, 255, cv2.THRESH_BINARY)
    # # ret, mask3 = cv2.threshold(gray_eye, 175, 255, cv2.THRESH_BINARY)
    #
    # ## gray mask
    # ret, mask4 = cv2.threshold(gray_eye, 100, 100, cv2.THRESH_BINARY)
    #
    # # hsv_color1 = np.asarray([0, 0, 255])   # white!
    # # hsv_color2 = np.asarray([30, 255, 255])   # yellow! note the order
    #
    # hsv_color1 = np.array([45, 100, 100])   # green!
    # hsv_color2 = np.array([75, 255, 255])   # green! note the order
    #
    # mask_6 = cv2.inRange(hsv_image,hsv_color1,hsv_color2)
    #
    # # lower_blue = np.array([110,50,50])
    # # upper_blue = np.array([130,255,255])
    #
    # lower_white = np.array([0, 0, 150])
    # upper_white = np.array([180, 150, 255])
    #
    # lower_blue = np.array([100,50,50])
    # upper_blue = np.array([140,255,255])
    #
    # mask_7 = cv2.inRange(hsv_image,lower_blue,upper_blue)
    # mask_8 = cv2.inRange(hsv_image,lower_white,upper_white)
    #
    # green_masked = cv2.bitwise_and(hsv_image,hsv_image, mask = mask_6)
    # blue_masked = cv2.bitwise_and(hsv_image,hsv_image, mask = mask_7)
    # white_masked = cv2.bitwise_and(hsv_image,hsv_image, mask = mask_8)

    # cv2.imshow('mask8', mask_8)
    # cv2.imshow('mask7', gray_eye)

    circles = cv2.HoughCircles(gray_eye,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=50,maxRadius=150)

    # circles = np.uint16(np.around(circles))

    # print('circles is ', circles)

    if circles is not None:
        # print('yes it is not none')

        circles = np.uint16(np.around(circles))

        inliers  = free_from_outliers(circles[0])

        x_mean = np.mean(inliers[:,0])
        y_mean = np.mean(inliers[:,1])
        r_mean = np.mean(inliers[:,2])

        # print('all',circles[0][:,0].size, 'inliers',inliers[:,0].size)
        # print()
        # print(hcas)

        cv2.circle(gray_eye,(np.int(x_mean),np.int(y_mean)),np.int(r_mean),(0,255,0),2)


        # for i in inliers:
        #
        #     # draw the outer circle
        #     cv2.circle(gray_eye,(i[0],i[1]),i[2],(0,255,0),2)
        #     # draw the center of the circle
        #     cv2.circle(gray_eye,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('detected circles',gray_eye)


    # cv2.imshow('hsv', white_masked)


    # mask5 = cv2.bitwise_or(mask3,mask4)
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

    # eye_masked = cv2.bitwise_not(roi,roi, mask = mask5)
    # eye_masked1 = cv2.bitwise_not(eye_masked,eye_masked, mask = mask4)


    # equa_img = cv2.equalizeHist(gray_eye[:,:,2])

    # cv2.imshow('press', equa_img)
    # cv2.imshow('press', hsv_image)
    # cv2.imshow('press1', mask_7)
    # cv2.imshow('hsv', hsv_image)

    # cv2.imshow('thres', corner)
    cv2.waitKey(0)

    if cv2.waitKey(25) & 0xff == 27:  # To get the correct frame rate
        cv2.destroyAllWindows()
        break




    count += 1
