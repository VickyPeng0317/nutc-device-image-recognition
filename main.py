from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from logic import getLCDTopNum, getQrcodeImg, getLCDImg, getLCDTopNum, getLCDDownNum
from base import pipe, trans  
from PIL import Image
from pyzbar.pyzbar import decode
import os
import shutil


# # 讀取圖片
# image = cv2.imread("img/1.png")

# # # #https://stackoverflow.com/questions/27233351/how-to-decode-a-qr-code-image-in-preferably-pure-python
# # # qrcodeImg = getQrcodeImg(image)
# # # qrcodeData = decode(qrcodeImg)[0].data
# # # print(f'QRCode data:{qrcodeData}')

# lcdImg = getLCDImg(image)
# num = getLCDNum(lcdImg)
# print(num)
def test_qrcode(count = 50):
    shutil.rmtree('output/FAILQR')
    os.mkdir('output/FAILQR')

    success = []
    fail = []
    for i in range(count):
        try:
            image = cv2.imread(f"img/{str(i+1)}.png")
            qrcodeImg = getQrcodeImg(image)
            qrcodeData = decode(qrcodeImg)[0].data
            success.append(i+1)
        except:
            cv2.imwrite(f'output/FAILQR/{str(i+1)}-qrcode.png', qrcodeImg)
            fail.append(i+1)
        
    print(f'success: {len(success)}, fail: {len(fail)}')
    print(fail)

def test_getLCDImg(start = 1, count = 50):
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img/{start}.png"))
        cv2.imshow(f'{str(start)}-lcdImg', lcdImg)
        start = start + 1

def test_getTopNumber(start = 1, count = 50):
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img/{start}.png"))
        print(f"{start}: {getLCDTopNum(lcdImg)}")
        start = start + 1

def test_getDownNumber(start = 1, count = 50):
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img/{start}.png"))
        print(f"{start}: {getLCDDownNum(lcdImg)}")
        start = start + 1

cv2.waitKey(0)