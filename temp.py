from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from base import pipe, trans  
from PIL import Image
from pyzbar.pyzbar import decode
from dbService import selectDevice
import json
from tempLogic import getQrcodeImg

test = 19
image = cv2.imread(f"img2/{str(test)}.jpg")
print(f'\n')
qrcodeImg = getQrcodeImg(image)
cv2.imshow('qrcodeImg', qrcodeImg)
cv2.waitKey(0)