import cv2
import numpy as np

cap = cv2.VideoCapture("video2.mp4")
cv2.namedWindow("Frame")
minn = np.ones((2,2))
count = 0


def gammaCorrection(image, g=1):
    ig = 1 / g
    lut = (np.arange(256) / 255) ** ig * 255
    lut = lut.astype("uint8")
    return cv2.LUT(image, lut)


while cap.isOpened():
    ret, frame = cap.read()

    blurred = gammaCorrection(frame)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

    thresh = cv2.erode(thresh, minn, iterations=4)
    thresh = cv2.dilate(thresh, minn, iterations=2)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(hierarchy) > 0:
        contours = contours[2:]
    #     cv2.drawContours(frame, contours, -1, (255,0,0), 3, cv2.LINE_AA, hierarchy[1:], 1)

    if len(contours) == 12:
        count += 1

    if count == 10:
        while True:
            cv2.putText(frame, f"This is my picture", (10, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 0, 0), 2)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
        break

    if ret:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()