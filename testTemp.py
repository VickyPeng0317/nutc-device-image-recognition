from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from tempLogic import getQrcodeImg, getLCDImg, getLCDNum
from base import pipe, trans  
from PIL import Image
from pyzbar.pyzbar import decode
import os
import shutil

def test_qrcode(start = 1, count = 50):
    # shutil.rmtree('output/FAILTEMPQR')
    # os.mkdir('output/FAITEMPLQR')

    success = []
    fail = []
    for i in range(count):
        try:
            image = cv2.imread(f"img2/{str(start+i)}.jpg")
            qrcodeImg = getQrcodeImg(image)
            qrcodeData = decode(qrcodeImg)[0].data
            success.append(start+i)
        except:
            cv2.imwrite(f'output/FAILTEMPQR/{str(start+i)}-qrcode.jpg', qrcodeImg)
            fail.append(start+i)
        
    print(f'success: {len(success)}, fail: {len(fail)}')
    print(fail)

def test_getLCDImg(start = 1, count = 50):
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img2/{start}.jpg"))
        cv2.imshow(f'{str(start)}-lcdImg', lcdImg)
        start = start + 1

def test_getNumber(start = 1, count = 50):
    fail = []
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img2/{start}.jpg"))
        num = getLCDNum(lcdImg)
        print(f"{start}: {num}")
        ansNum = ans[start-1]
        if num != ansNum:
            fail.append(f'{start}. Ans: {ansNum}, Current: {num}')
        start = start + 1
    showTestAns(fail, count)

def showTestAns(failArr, allCount):
    for data in failArr:
        print(data)
    failCount = len(failArr)
    successCount = allCount - failCount
    print(f'圖像總數: {allCount}\n辨識成功: {successCount}\n辨識失敗: {failCount}\n辨識成功率: {(successCount/allCount)*100}%')

ans = [
    '38.1',
    '38.2',
    '38.3',
    '38.4',
    '38.5',
    '38.6',
    '38.7',
    '38.8',
    '38.9',
    '39.0',
    # 10
    '39.0',
    '39.0',
    '39.0',
    '39.0',
    '37.6',
    '38.0',
    '38.4',
    '38.5',
    '38.6',
    '38.9'
]