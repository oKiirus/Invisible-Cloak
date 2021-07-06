import cv2 
import time
import numpy as np

video = cv2.VideoWriter_fourcc(*'XVID')
file = cv2.VideoWriter('video.avi', video, 30, (1028, 1028))
capture = cv2.VideoCapture(0)
time.sleep(2)
bg = 0


for i in range(0, 60):
    ret, bg = capture.read()

bg = np.flip(bg, axis = 1)

while(capture.isOpened()):
    
    ret, img = capture.read()

    if not ret:
        break

    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerRed = np.array([0, 120, 50])
    upperRed = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lowerRed, upperRed)
    lowerRed = np.array([170, 120, 50])
    upperRed = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lowerRed, upperRed)
    mask = mask1 + mask2
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    result1 = cv2.bitwise_and(img, img, mask = mask2)
    result2 = cv2.bitwise_and(bg, bg, mask = mask1)
    output = cv2.addWeighted(result1, 1, result2, 1, 0)
    file.write(output)
    cv2.imshow('Magic', output)
    cv2.waitKey(1)
capture.release()
cv2.destroyAllWindows()