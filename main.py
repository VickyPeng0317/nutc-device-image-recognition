from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from logic import getQrcodeImg, getLCDImg, getLCDNum
from base import pipe, trans  
from PIL import Image
from pyzbar.pyzbar import decode

# 讀取圖片
image = cv2.imread("img/ccc2.png")

#https://stackoverflow.com/questions/27233351/how-to-decode-a-qr-code-image-in-preferably-pure-python
qrcodeImg = getQrcodeImg(image)
qrcodeData = decode(qrcodeImg)[0].data
print(f'QRCode data:{qrcodeData}')

lcdImg = getLCDImg(image)
num = getLCDNum(lcdImg)