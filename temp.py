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

test = 11
image = cv2.imread(f"img2/{str(test)}.jpg")
# print(f'\n')
# qrcodeImg = getQrcodeImg(image)
# qrcodeData = decode(qrcodeImg)[0].data
# qrcodeDataJson = json.loads((str(qrcodeData)).split("b\'")[1].split("\'")[0])
# deviceId = qrcodeDataJson['deviceId']
# print('-------設備 QRCode 識別結果------')
# print(f'QRCode 資料: {qrcodeDataJson}')
# print(f'\n')


cv2.waitKey(0)