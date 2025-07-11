from ultralytics import YOLO
import cvzone
import math
import cv2
from sort import *

cap = cv2.VideoCapture("../video/cars.mp4")  # For Video


model = YOLO("../yoloweight/yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

mask = cv2.imread("mask.png")


#tracking
tracker = Sort(max_age=20,min_hits=3,iou_threshold=0.3)
totalCount=[]
limits = [400,297,673,297]
while True:

    success, img = cap.read()
    imageregion=cv2.bitwise_and(img,mask)
    graphics=cv2.imread("graphics.png",cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img,graphics,(0,0))

    results = model(imageregion, stream=True)

    detections = np.empty((0,5))
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentclass=classNames[cls]


            #what to detect
            if currentclass == "car" or currentclass == "motorbike" or currentclass == "truck" or currentclass == "bus" and conf > 0.3:
                #cvzone.putTextRect(img, f'{currentclass} {conf}', (max(0, x1), max(35, y1)), scale=0.6
                #                   , thickness=1, offset=3)
                #cvzone.cornerRect(img, (x1, y1, w, h), l=9,rt=5)
                currentArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack([detections, currentArray])

    resultTracker = tracker.update(detections)
    cv2.line(img,(limits[0],limits[1]),(limits[2],limits[3]),(0,0,255),2)

    for result in resultTracker:
        x1,y1,x2,y2,id = result
        print(result)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        #the blue rectangle and info
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2,colorR=(255,0,0))
        cvzone.putTextRect(img, f'{int(id)} ', (max(0, x1), max(35, y1)), scale=2
                           , thickness=3, offset=10)

        cx,cy = x1+w//2, y1+h//2
        cv2.circle(img,(cx,cy),5,(0,255,0),cv2.FILLED)

        if limits[0]<cx<limits[2] and limits[1]-15<cy<limits[1]+15:
            if totalCount.count(id)==0:
                totalCount.append(id)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 2)


    #cvzone.putTextRect(img, f' Count: {len(totalCount)} ',(50,50))
    cv2.putText(img,str(len(totalCount)),(255,100),cv2.FONT_HERSHEY_PLAIN,5,(50,50,255),8)


    cv2.imshow("Image", img)
    cv2.waitKey(0)