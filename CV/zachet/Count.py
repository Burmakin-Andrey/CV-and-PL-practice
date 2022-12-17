import numpy as np
from skimage.measure import label
import cv2

def gammaCorrection(image, g=1):
    ig = 1 / g
    lut = (np.arange(256) / 255) ** ig * 255
    lut = lut.astype("uint8")
    return cv2.LUT(image, lut)

minn = np.ones((6,6))
cap = cv2.VideoCapture("balls.mp4")
count = 0
prev_count = 0
cv2.namedWindow("Frame")

while cap.isOpened():
    ret, frame = cap.read()

    blurred = gammaCorrection(frame)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    thresh = cv2.erode(thresh, minn, iterations=4)
    thresh = cv2.dilate(thresh, minn, iterations=2)
    lebled = label(thresh)    

    count = lebled.max()
    if count <= 5:
        prev_count = count
    else:
        count = prev_count


    cv2.putText(frame, f"Count balls {count}", (50, 50),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
    cv2.imshow('Frame', frame)
    
 
                                                             
    # cv2.imshow("thresh", thresh)
    key = cv2.waitKey(1) 
    if key == ord('q'):
        break
cv2.destroyAllWindows()