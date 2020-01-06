import cv2
import numpy as np
from easygraphics import *
import qimage2ndarray

def main():
    init_graph(800,600)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color("white")
    print("init_camera")
    success, frame = cameraCapture.read()
    print("init_camera_ok")
    while is_run() and success:
        height, width, bytesPerComponent = frame.shape
        img : np.ndarray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image = Image(qimage2ndarray.array2qimage(img))
        draw_image(0,0,image)
        image.close()
        delay_fps(30)
        success, frame = cameraCapture.read()


cameraCapture = cv2.VideoCapture(0)
# force the camera to use MJPG format, or it will be very slow to capture
cameraCapture.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
easy_run(main)
cameraCapture.release()