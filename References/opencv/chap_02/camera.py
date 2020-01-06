import cv2
import numpy as np

cameraCapture = cv2.VideoCapture(0)
# force the camera to use MJPG format, or it will be very slow to capture
cameraCapture.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
cv2.namedWindow("MyWindow")
success,frame = cameraCapture.read()

while success:
    cv2.imshow("MyWindow",frame)
    if cv2.waitKey(1)!=-1:
        break
    success,frame = cameraCapture.read()
cameraCapture.release()