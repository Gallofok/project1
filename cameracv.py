import cv2 
import numpy as np
framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)

cap.set(3,framewidth)
cap.set(4,frameheight)
def empty(a):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
cv2.createTrackbar("Threshold2","Parameters",20,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)

def getcounters(img,imgCounter):
    counters,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    areamin = cv2.getTrackbarPos("Area","Parameters")
    for cnt in counters:
        area = cv2.contourArea(cnt)
        if area > areamin:
            cv2.drawContours(imgCounter,cnt,-1,(255,0,255),7)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgCounter,(x,y),(x+w,y+h),(0,255,0),5)
            #cv2.putText(imgCounter,'points: ' + str(len(approx)),(x+w+20,y+20),cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            #cv2.putText(imgCounter,'Area: ' + str(area),(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            cv2.putText(imgCounter,'Area: ' + str(area),(x+w//2,y+h//2),cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
while True :
    _,frame = cap.read()
    fraCounter = frame.copy()

    frameBlur = cv2.GaussianBlur(frame,(7,7,),1) 
    frameGray = cv2.cvtColor(frameBlur,cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")
    frameCanny = cv2.Canny(frameGray,threshold1,threshold2)
    kernel = np.ones((5,5))
    fraDil = cv2.dilate(frameCanny,kernel,iterations=1)
    getcounters(fraDil,fraCounter)

    cv2.imshow("res",fraCounter)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
