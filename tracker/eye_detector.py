import cv2

eye_detector = cv2.CascadeClassifier('haarcascade_eye.xml')

eye_image_path = 'resources/frames/frame0.jpg'

eye_image = cv2.imread(eye_image_path)

# gray_eye_image = cv2.cvtColor(eye_image, cv2.COLOR_BGR2GRAY)

cv2.imshow('eye', eye_image)
cv2.waitKey(0)

eyes = eye_detector.detectMultiScale(eye_image)
