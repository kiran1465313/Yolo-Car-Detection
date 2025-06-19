from ultralytics import YOLO
import cv2

model = YOLO('../yoloweight/yolov8l.pt')
results = model("images/1.png", show=True)
cv2.waitKey(0)