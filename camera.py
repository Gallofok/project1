import cv2
import torch
import numpy as np
import keyboard
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, customp
path1 = 'E:/kosys/project1/yolov5'
path2 = 'E:/kosys/project1/plate.pt'
model = torch.hub.load(path1,'custom', path= path2, source='local')


dis = [ 997,992,987,982,977,972]

diag = [290,300,312,320,331,345]

A,B= np.polyfit(diag,dis,1)

# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (50, 50)
  
# fontScale
fontScale = 1
   
# Blue color in BGR
color = (255, 0, 0)
  
# Line thickness of 2 px
thickness = 2




while True :

    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_AREA)
    
    # Inference
    results = model(frame)

    results = results.pandas().xyxy[0].to_dict(orient="records")
    for result in results:
                con = result['confidence']
                cs = result['class']
                name = result['name']
                #if name == 'stock' and con > 0.5:
                x1 = int(result['xmin'])
                y1 = int(result['ymin'])
                x2 = int(result['xmax'])
                y2 = int(result['ymax'])
                #get the diagonal size
                # diago =int(np.sqrt((x2-x1)**2 + (y2-y1)**2))
                # objdis = 'distance is   ' + str(int(A*diago+B)/10)+ '  cm '
                output = name + ': ' + str(int(con*100))+'%'
                frame = cv2.putText(frame, output, (x1,y1), font,fontScale, color, thickness, cv2.LINE_AA)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)


    cv2.imshow('Input', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break


cap.release()
cv2.destroyAllWindows()



