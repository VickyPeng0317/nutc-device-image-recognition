from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from tempLogic import sevenDisplayNum, getQrcodeImg, getLCDImg, getLCDNum, getLCDNumImgArr
from base import pipe, trans  
from PIL import Image
from pyzbar.pyzbar import decode
import os
import shutil
from datetime import datetime

def test_qrcode(start = 1, count = 50):
    # shutil.rmtree('output/FAILTEMPQR')
    # os.mkdir('output/FAITEMPLQR')
    start_time = datetime.now()
    print("Start Time =", start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

    success = []
    fail = []
    for i in range(count):
        try:
            image = cv2.imread(f"img2/{str(start+i)}.jpg")
            qrcodeImg = getQrcodeImg(image)
            qrcodeData = decode(qrcodeImg)[0].data
            success.append(start+i)
            # cv2.imwrite(f'output/TEMPQR/{str(start+i)}-qrcode.jpg', qrcodeImg)
        except:
            # cv2.imwrite(f'output/TEMPQR/{str(start+i)}-qrcode.jpg', qrcodeImg)
            fail.append(start+i)
    after_time = datetime.now()
    print("After Time =", after_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    print((after_time-start_time))
    print(f'success: {len(success)}, fail: {len(fail)}')
    print(fail)

def test_getLCDImg(start = 1, count = 50):
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img2/{start}.jpg"))
        cv2.imshow(f'{str(start)}-lcdImg', lcdImg)
        start = start + 1

def test_getNumber(start = 1, count = 50):
    start_time = datetime.now()
    print("Start Time =", start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    fail = []
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img2/{start}.jpg"))
        num = getLCDNum(lcdImg)
        print(f"{start}: {num}")
        ansNum = ans[start-1]
        if num != ansNum:
            fail.append(f'{start}. Ans: {ansNum}, Current: {num}')
        start = start + 1
    after_time = datetime.now()
    print("After Time =", after_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    print((after_time-start_time))
    # showTestAns(fail, count)

def test_getLCDNumImgArr(start = 1, count = 50):
    start_time = datetime.now()
    print("Start Time =", start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    all = 0
    final = 0
    success = 0
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img2/{start}.jpg"))
        numImgArr = getLCDNumImgArr(lcdImg)
        numData = ans[start-1]
        # 計算 Top 切割圖像準確率
        numData2 = ''.join(numData.split('.'))
        for index in range(len(numImgArr)):
            numValue = sevenDisplayNum(numImgArr[index])
            if (numData2[index] == numValue):
                success += 1
        all += (len(numData) - 1)
        final += len(numImgArr)
        start = start + 1
    print(f'all {all}')
    print(f'final {final}')
    print(f'success {success}')
    after_time = datetime.now()
    print("After Time =", after_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    print((after_time-start_time))

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
    '38.9',
    # 20
    '36.2', 
    '36.2', 
    '35.8', 
    '35.8', 
    '35.9', 
    '35.9', 
    '36.1', 
    '36.6', 
    '36.1', 
    '36.3', 
    # 30
    '36.3', 
    '36.3', 
    '36.3', 
    '36.2', 
    '36.2', 
    '36.3', 
    '36.3', 
    '36.2', 
    '36.2', 
    '36.2', 
    # 40
    '36.5', 
    '36.6', 
    '36.3', 
    '36.5', 
    '36.5', 
    '36.5', 
    '35.8', 
    '35.8', 
    '35.8', 
    '36.4', 
    # 50
    '36.4', 
    '36.4', 
    '36.6', 
    '36.6', 
    '36.6', 
    '36.2', 
    '36.2', 
    '36.2', 
    '36.3', 
    '36.3', 
    # 60
    '36.3', 
    '36.4', 
    '36.4', 
    '36.4', 
    '35.9', 
    '35.9', 
    '35.9', 
    '36.3', 
    '36.3', 
    '36.3', 
    # 70
    '36.3', 
    '36.3', 
    '36.3', 
    '36.4', 
    '36.4', 
    '36.4', 
    '35.9', 
    '35.9', 
    '35.9', 
    '36.2', 
    # 80
    '36.2', 
    '36.2', 
    '36.3', 
    '36.3', 
    '36.3', 
    '36.2', 
    '36.2', 
    '36.2', 
    '36.6', 
    '36.6', 
    # 90
    '36.6', 
    '36.2', 
    '36.2', 
    '36.2', 
    '36.6', 
    '36.6', 
    '36.6', 
    '36.2', 
    '36.2', 
    '36.2'
]