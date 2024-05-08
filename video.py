import cv2
import pickle
import numpy as np
#import cvzone

#Video feed

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPosition', 'rb') as f:
        posList = pickle.load(f)
#height of the rectangle boxes
width, height = 90, 40

def checkParkingSpace(imgPro):
     spaceCounter = 0
     
     
     for pos in posList:
        x, y = pos
        scale = 3
        thickness = 5
        offset = 20
        colorR = (0, 200, 0) 

        # Get the text size
        text = str(spaceCounter)
        font = cv2.FONT_HERSHEY_SIMPLEX

        imgCrop = imgPro[y:y+height, x:x+width]
        cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cv2.putText(img, str(count), (x, y + height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        if count < 700:
             color = (0,255,0)
             thickness = 5
             spaceCounter += 1
        else:
             color = (0,0,255)
             thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        
     cv2.putText(img, f' {text}/{len(posList)}', (x + offset // 2 - 1000, y - offset // 2 - 550), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3, 3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations = 1)
    checkParkingSpace(imgDilate)

    cv2.imshow("image", img)
    cv2.imshow("ImageBlur", imgBlur)
    cv2.imshow("ImageThreshold", imgMedian)
    cv2.waitKey(10)