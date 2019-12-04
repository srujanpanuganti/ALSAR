import cv2
import numpy as np
from scipy import stats
import time
import sys

vidcap = cv2.VideoCapture('resources/eye.mp4')
# vidcap = cv2.VideoCapture(0)

# if not vidcap.isOpened():
#     print("[ERROR] : Could not open video, camera isn't working")
#     sys.exit()
# else:
#     print('[INFO] : camera working')

# success,image = vidcap.read()
count = 0

previous_frame = 0
current_frame = 0

def detect_eye(image):
    eye_detector = cv2.CascadeClassifier('resources/haarcascade_eye.xml')
    eyes = eye_detector.detectMultiScale(image)

    print(eyes)

    current_bounding_box = eyes[0]
    # p1 = (int(current_bounding_box[0]), int(current_bounding_box[1]))
    # p2 = (int(current_bounding_box[0] + current_bounding_box[2]), int(current_bounding_box[1] + current_bounding_box[3]))
    return current_bounding_box

def good_key_points(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)

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

def get_pupil_center(img):

    ret, thresh = cv2.threshold(img, 125, 255, cv2.THRESH_TRUNC)

    circles = cv2.HoughCircles(thresh,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=50,maxRadius=150)

    if circles is not None:

        circles = np.uint16(np.around(circles))

        # print(circles[0].size)

        inliers  = free_from_outliers(circles[0])

        x_mean = np.mean(inliers[:,0])
        y_mean = np.mean(inliers[:,1])
        r_mean = np.mean(inliers[:,2])

        # cv2.circle(roi,(np.int(x_mean),np.int(y_mean)),np.int(r_mean),(255,255,100),2)

        pupil_center = (np.int(x_mean),np.int(y_mean), np.int(r_mean))

        return pupil_center

def generate_command(pupil_center, eye_center):

    e_c = eye_center
    x_e_c = e_c[0]
    y_e_c = e_c[1]

    p_c = pupil_center

    print(p_c)

    x_p_c = p_c[0]
    y_p_c = p_c[1]

    x_thresh = 50
    y_thresh = 30


    ###################################################################################################
    ####### The go straight and go back are working opposite, need to change that #######################

    if x_p_c > (x_e_c - x_thresh) and x_p_c < (x_e_c + x_thresh):

        if y_p_c >= (y_e_c + y_thresh):

            print('go straight')
            command = 'go straight'

        elif y_p_c <= (y_e_c - y_thresh):

            print('go back')
            command = 'go back'

        else:
            print('stay idle')
            command = 'stay idle'

    elif x_p_c < (x_e_c - x_thresh):

        print('turn right')
        command = 'turn right'

    elif x_p_c > (x_e_c + x_thresh):

        print('turn left')
        command = 'turn left'

    else:

        print('dont know where to go')
        command = 'dont know where to go'

    # return command


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

    status,image = vidcap.read()

    # time.sleep(2.0)

    timer = cv2.getTickCount()


    if status:

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
        #
        # eyes = detect_eye(image)


        # x = eyes[0]
        # y = eyes[1]
        # w = eyes[2]
        # h = eyes[3]

        p1 = x
        p2 = y
        p1w = w
        p2h = h

        roi = image[p2:p2+p2h, p1:p1+p1w]

        roi_center = (roi.shape[0]/2, roi.shape[1]/2)

        # print(roi_center)

        gray_eye = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        hsv_image = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # ## white mask
        # thresh = cv2.adaptiveThreshold(gray_eye, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,0.5)

        # ret, thresh = cv2.threshold(gray_eye, 125, 255, cv2.THRESH_TRUNC)

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

        pupil_cen = get_pupil_center(gray_eye)

        if pupil_cen:
            generate_command(pupil_cen, roi_center)
            cv2.circle(roi,(pupil_cen[0],pupil_cen[1]),pupil_cen[2],(255,255,100),2)

        # else:
        #     cv2.destroyAllWindows()
        #     break
        cv2.imshow('detected circles',roi)
        # cv2.imshow('hsv', white_masked)

        cv2.waitKey(0)

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
        # cv2.waitKey(5)

        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # print(fps)

        if cv2.waitKey(25) & 0xff == 27:  # To get the correct frame rate
            cv2.destroyAllWindows()
            break

        count += 1

    else:
        cv2.destroyAllWindows()
        break
