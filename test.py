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

def test_qrcode(start = 1, count = 50):
    shutil.rmtree('output/FAILQR')
    os.mkdir('output/FAILQR')

    success = []
    fail = []
    for i in range(count):
        try:
            image = cv2.imread(f"img/{str(i+start)}.png")
            qrcodeImg = getQrcodeImg(image)
            qrcodeData = decode(qrcodeImg)[0].data
            success.append(i+start)
        except:
            cv2.imwrite(f'output/FAILQR/{str(i+start)}-qrcode.png', qrcodeImg)
            fail.append(i+start)
        
    print(f'success: {len(success)}, fail: {len(fail)}')
    print(fail)

def test_getLCDImg(start = 1, count = 50):
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img/{start}.png"))
        cv2.imshow(f'{str(start)}-lcdImg', lcdImg)
        start = start + 1

def test_getTopNumber(start = 1, count = 50):
    fail = []
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img/{start}.png"))
        topNum = getLCDTopNum(lcdImg)
        print(f"{start}: {topNum}")
        ansNum = ans[start-1][0]
        if topNum != ansNum:
            fail.append(f'{start}. Ans: {ansNum}, Current: {topNum}')
        start = start + 1
    showTestAns(fail, count)


def test_getDownNumber(start = 1, count = 50):
    fail = []
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img/{start}.png"))
        downNum = getLCDDownNum(lcdImg)
        print(f"{start}: {downNum}")
        ansNum = ans[start-1][1]
        if downNum != ansNum:
            fail.append(f'{start}. Ans: {ansNum}, Current: {downNum}')
        start = start + 1
    showTestAns(fail, count)

def test_getAllNumber(start = 1, count = 50):
    fail = []
    for _ in range(count):
        lcdImg = getLCDImg(cv2.imread(f"img/{start}.png"))
        topNum = getLCDTopNum(lcdImg)
        downNum = getLCDDownNum(lcdImg)
        print(f"{start}: {topNum}, {downNum}")
        [topAnsNum, downAnsNum] = ans[start-1]
        if (topNum != topAnsNum) or (downNum != downAnsNum):
            fail.append(f'{start}. {topAnsNum}->{topNum}, {downAnsNum}->{downNum}')
        start = start + 1
    showTestAns(fail, count)

def showTestAns(failArr, allCount):
    for data in failArr:
        print(data)
    failCount = len(failArr)
    successCount = allCount - failCount
    print(f'圖像總數: {allCount}\n辨識成功: {successCount}\n辨識失敗: {failCount}\n辨識成功率: {(successCount/allCount)*100}%')

ans = [
    #0
    ['110', '65'],
    ['123', '82'],
    ['133', '82'],
    ['122', '72'],
    ['122', '86'],
    ['135', '85'],
    ['118', '77'],
    ['119', '77'],
    ['120', '78'],
    ['120', '78'],
    #10
    ['121', '76'],
    ['120', '77'],
    ['109', '75'],
    ['123', '73'],
    ['110', '46'],
    ['119', '77'],
    ['119', '76'],
    ['118', '75'],
    ['118', '75'],
    ['122', '74'],
    #20
    ['96', '61'],
    ['119', '78'],
    ['120', '80'],
    ['119', '79'],
    ['121', '80'],
    ['120', '80'],
    ['120', '79'],
    ['122', '81'],
    ['118', '78'],
    ['96', '65'],
    #30
    ['118', '75'],
    ['122', '76'],
    ['120', '74'],
    ['120', '74'],
    ['118', '61'],
    ['119', '74'],
    ['112', '68'],
    ['130', '81'],
    ['102', '69'],
    ['112', '70'],
    #40
    ['113', '71'],
    ['113', '71'],
    ['95', '67'],
    ['183', '69'],
    ['109', '70'],
    ['130', '82'],
    ['127', '81'],
    ['125', '79'],
    ['102', '61'],
    ['103', '59'],
    #50
    ['122', '87'],
    ['122', '87'],
    ['135', '88'],
    ['135', '88'],
    ['102', '82'],
    ['102', '82'],
    ['126', '92'],
    ['126', '92'],
    ['138', '90'],
    ['138', '90'],
    #60
    ['136', '89'],
    ['136', '89'],
    ['137', '89'],
    ['137', '89'],
    ['139', '89'],
    ['139', '89'],
    ['116', '73'],
    ['116', '73'],
    ['133', '88'],
    ['133', '88'],
    #70
    ['146', '91'],
    ['146', '91'],
    ['127', '93'],
    ['127', '93'],
    ['124', '69'],
    ['124', '69'],
    ['123', '71'],
    ['123', '71'],
    ['147', '88'],
    ['147', '88'],
    #80
    ['113', '69'],
    ['113', '69'],
    ['131', '84'],
    ['131', '84'],
    ['136', '83'],
    ['136', '83'],
    ['134', '82'],
    ['134', '82'],
    ['134', '83'],
    ['134', '83'],
    #90
    ['102', '71'],
    ['102', '71'],
    ['127', '70'],
    ['127', '70'],
    ['131', '89'],
    ['131', '89'],
    ['116', '80'],
    ['116', '80'],
    ['129', '78'],
    ['129', '78'],
    #100
    ['113', '71'],
    ['113', '71'],
    ['95', '67'],
    ['183', '69'],
    ['109', '70'],
    ['130', '82'],
    ['127', '81'],
    ['125', '79'],
    ['102', '61'],
    ['103', '59'],
    #110
    ['113', '71'],
    ['113', '71'],
    ['95', '67'],
    ['183', '69'],
    ['109', '70'],
    ['130', '82'],
    ['127', '81'],
    ['125', '79'],
    ['102', '61'],
    ['103', '59'],
    #120
    ['113', '71'],
    ['113', '71'],
    ['95', '67'],
    ['183', '69'],
    ['109', '70'],
    ['130', '82'],
    ['127', '81'],
    ['125', '79'],
    ['102', '61'],
    ['103', '59'],
    #130
    ['113', '71'],
    ['113', '71'],
    ['95', '67'],
    ['183', '69'],
    ['109', '70'],
    ['130', '82'],
    ['127', '81'],
    ['125', '79'],
    ['102', '61'],
    ['103', '59'],
    #140
    ['113', '71'],
    ['113', '71'],
    ['95', '67'],
    ['183', '69'],
    ['109', '70'],
    ['130', '82'],
    ['127', '81'],
    ['125', '79'],
    ['102', '61'],
    ['103', '59'],
]