import cv2

vidcap = cv2.VideoCapture('resources/eye.mp4')
success,image = vidcap.read()
count = 0
success = True
while success:
  # cv2.imwrite("resources/frames/frame%d.jpg".format(count, image))     # save frame as JPEG file
  cv2.imwrite("resources/frames/pic{:>05}.jpg".format(count), image)
  print('frame%d.jpg')
  success,image = vidcap.read()
  count += 1
