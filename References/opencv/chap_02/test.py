import cv2
import numpy as np

img = np.zeros((100,100),dtype=np.uint8)

img =cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
print(img[0,0,0])
for i in range(10):
    for j in range(10):
        img[i,j]=[255,255,255]
cv2.imshow('my image', img)
print("lala")
cv2.waitKey()
cv2.destroyAllWindows()