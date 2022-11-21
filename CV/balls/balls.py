import cv2
import numpy as np
import random
 
ball_bl = [98, 232, 120]
ball_gr = [60, 150, 110]
ball_re = [0, 255, 150]
balls = [ball_bl, ball_gr, ball_re]
# names = {ball_bl: "Blue",ball_gr: "Green", ball_re: "Red"}

def random_sequence():
    seque = [0,1,2]
    seques = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if(i != j & j != k & k != i):
                    seques.append([seque[i], seque[j], seque[k]])
    return seques[random.randint(0, 10) % 6]


task = random_sequence()

lower = []
higher = []

for ball in balls:
    lower.append(np.array([ball[0] - 15, ball[1] - 50, 0]))
    higher.append(np.array([ball[0] + 15, ball[1] + 50, 255]))


def make_mask(frame, low, high, iD):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low[iD], high[iD])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    return mask
 
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cam.set(cv2.CAP_PROP_EXPOSURE, -4)
 
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
 
low_hig = []
masks = []
while cam.isOpened():
    ret,frame = cam.read()
    iD_pos = []
    iD = 0
    for ball in balls:
        mask = make_mask(frame, lower, higher, iD)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        iD += 1
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            iD_pos.append(x)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

    if len(iD_pos) == 3:
        if iD_pos[task[0]] < iD_pos[task[1]] < iD_pos[task[2]]:
            print("Угадали")
            # print("Правильная последовательность:", names.get(balls[task[0]]), names.get(balls[task[1]]), names.get(balls[task[2]]))
        else:
            # print("Не угдал")
            print(task)
    
            
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
    cv2.imshow("Camera", frame)
    #cv2.imshow("Mask", mask)


cam.release()
cv2.destroyAllWindows()
