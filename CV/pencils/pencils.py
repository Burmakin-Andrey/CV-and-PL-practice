import numpy as np
import cv2

count = 0

for i in range(1, 13):
    
    gray = cv2.imread(f"images/img ({i}).jpg", cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(gray, (91, 91), 0)
    _, thresh = cv2.threshold(blurred, 125, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        rect = cv2.minAreaRect(c)
        width = rect[1][0]
        height = rect[1][1]
        if height * 5 < width:
            count += 1
        if width * 5 < height:
            count += 1

print("Pencils: ", count)