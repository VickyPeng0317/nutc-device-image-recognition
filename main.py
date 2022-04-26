from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from logic import getLCDTopNum, getQrcodeImg, getLCDImg, getLCDTopNum, getLCDDownNum
from base import pipe, trans  
from PIL import Image
from pyzbar.pyzbar import decode
from test import test_qrcode, test_getLCDImg, test_getTopNumber, test_getDownNumber, test_getAllNumber

# # 讀取圖片
# image = cv2.imread("img/1.png")

# # # #https://stackoverflow.com/questions/27233351/how-to-decode-a-qr-code-image-in-preferably-pure-python
# # # qrcodeImg = getQrcodeImg(image)
# # # qrcodeData = decode(qrcodeImg)[0].data
# # # print(f'QRCode data:{qrcodeData}')

# lcdImg = getLCDImg(image)
# num = getLCDNum(lcdImg)
# print(num)

test_getAllNumber(1, 50)
cv2.waitKey(0)