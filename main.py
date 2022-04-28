from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from logic import getLCDTopNum, getQrcodeImg, getLCDImg, getLCDTopNum, getLCDDownNum
from base import pipe, trans  
from PIL import Image
from pyzbar.pyzbar import decode
from test import test_qrcode, test_getLCDImg, test_getTopNumber, test_getDownNumber, test_getAllNumber, ans
from dbService import selectDevice
import json

# # # #https://stackoverflow.com/questions/27233351/how-to-decode-a-qr-code-image-in-preferably-pure-python
# # # qrcodeImg = getQrcodeImg(image)
# # # qrcodeData = decode(qrcodeImg)[0].data
# # # print(f'QRCode data:{qrcodeData}')

# 讀取圖片 27 29
test = 7
image = cv2.imread(f"img/{str(test)}.png")
print(f'\n')

qrcodeImg = getQrcodeImg(image)
qrcodeData = decode(qrcodeImg)[0].data
qrcodeDataJson = json.loads((str(qrcodeData)).split("b\'")[1].split("\'")[0])
deviceId = qrcodeDataJson['deviceId']
print('-------設備 QRCode 識別結果------')
print(f'QRCode 資料: {qrcodeDataJson}')
print(f'\n')

print('-------設備查詢結果------')
device = selectDevice(deviceId)
print(f'{"{:>4}".format("設備ID")}: {device["deviceId"]}')
print(f'{"{:>4}".format("設備名稱")}: {device["deviceName"]}')
print(f'{"{:>4}".format("設備位置")}: {device["deviceAddress"]}')
print(f'\n')

lcdImg = getLCDImg(image)
print('-------血壓影像辨識結果------')
print(f'收縮壓: {"{:>3}".format(getLCDTopNum(lcdImg))} mmHg')
print(f'舒張壓: {"{:>3}".format(getLCDDownNum(lcdImg))} mmHg')

print(f'\n')
# test_getAllNumber(1, 50)
cv2.waitKey(0)