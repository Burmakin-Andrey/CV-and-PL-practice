import numpy as np
import cv2
import time

# 110, 240, 240
low_blue = (95, 225, 225)
up_blue = (125, 255, 255)

minn = np.ones((6,6))
cap = cv2.VideoCapture(0)
prev_position = [0,0]
real_radius = 0.056
start = time.time()
cv2.namedWindow("Frame")

while cap.isOpened():
    time1 = time.time()
    ret, frame = cap.read()

    blurred = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, low_blue, up_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if prev_position == [0,0]:
            prev_position = [x, y]
        s_pixel = ((prev_position[0] - x) ** 2 + (prev_position[1] - y) ** 2) ** 0.5 
        s_meters = (s_pixel / (2*radius)) * real_radius
        prev_position = [x, y]
        t = start - time.time()
        v = round(s_meters * 30.3 / t, 3)

        cv2.putText(frame, f"Speed {v}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))





    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) 
    if key == ord('q'):
        break
cv2.destroyAllWindows()