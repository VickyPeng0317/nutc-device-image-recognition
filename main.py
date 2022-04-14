from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from logic import getQrcodeImg, getLCDImg, getLCDNum
from base import pipe, trans  

# 讀取圖片
image = cv2.imread("img/ccc2.png")
 
qrcodeImg = getQrcodeImg(image)

pipe(
    trans(lambda img: getLCDImg(img)),
    trans(lambda img: getLCDNum(img))
)(image)
