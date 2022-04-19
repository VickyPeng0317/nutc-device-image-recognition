from ast import Lambda
from re import X
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
from base import trans, tap, pipe
from lib import sharpen, modify_contrast_and_brightness2

def getQrcodeImg(image):
    # resize 500
    image = imutils.resize(image, height=500)

    # 灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('output/QR/1-cvtColor.png', gray)
    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite('output/QR/2-GaussianBlur.png', blurred)
    # 邊緣檢測
    edged = cv2.Canny(blurred, 50, 200, 255)
    cv2.imwrite('output/QR/3-Canny.png', edged)
    
    # 在邊緣檢測map中取得輪廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 依大小排序輪廓
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None
    
    # 讀取所有輪廓
    for c in cnts:
        # 對輪廓進行相似比對
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
        # 找出有四個頂點的輪廓
        if len(approx) == 4:
            displayCnt = approx
            break
    
    # 把圖切出來
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    cv2.imwrite('output/QR/origin-qrcode.png', warped)

    # 二值化
    thresh = cv2.threshold(warped, 100, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('output/QR/threshold-qrcode.png', thresh)
    return warped

def getLCDImg(image):
    (B, R, G) = cv2.split(image)
    cv2.imwrite('output/getNumber/ORIGIN.png', image)
    cv2.imwrite('output/getNumber/B.png', B)
    cv2.imwrite('output/getNumber/R.png', R)
    cv2.imwrite('output/getNumber/G.png', G)
    # 高斯模糊
    blurred = cv2.GaussianBlur(B, (5, 5), 0)
    cv2.imwrite('output/getNumber/B_1-blurred.png', blurred)
    # 邊緣檢測
    edged = cv2.Canny(blurred, 50, 200, 255)
    cv2.imwrite('output/getNumber/B_2-Canny.png', edged)

    # 在邊緣檢測map中取得輪廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 依大小排序輪廓
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    allApprox = []
    # 讀取所有輪廓
    for c in cnts:
        # 對輪廓進行相似比對
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
        # 找出有四個頂點的輪廓
        if len(approx) == 4:
            allApprox.append(approx)

    # 計算區域面積
    allApproxArea = [cv2.contourArea(approx) for approx in allApprox]
    # 取得最大面積索引
    lcdAreaIndex = np.argmax(allApproxArea, axis=0)
    # 切割 LCD 區塊
    lcdAreaImg = four_point_transform(image, allApprox[lcdAreaIndex].reshape(4, 2))
    cv2.imwrite(f'output/getNumber/LCD.png', lcdAreaImg)
    return lcdAreaImg

def getNumberImgFourPoint(img):
    # 找出輪廓
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 取得外接矩形
    boundingRectArr = np.array([cv2.boundingRect(c) for c in contours])

    # 取得最左上方座標
    [startX, startY, *_] = np.amin(boundingRectArr, axis=0)

    # 取得最右下方座標
    boundingRectEndPointArr = [[ar[0] + ar[2], ar[1] + ar[3]] for ar in boundingRectArr]
    [endX, endY, *_] = np.amax(boundingRectEndPointArr, axis=0)

    # 組出外接矩形4個座標， D 為矩形外擴閥值
    D = 1.05
    startX = int(startX / D)
    startY = int(startY / D)
    endX = int(endX * D)
    endY = int(endY * D)
    fourPoint = np.array([
        [startX, startY],
        [startX, endY],
        [endX, endY],
        [endX, startY],
    ])
    return fourPoint

def getTopNum(lcd_origin, lcd_pre):
    height = lcd_pre.shape[0]
    top = lcd_pre[0:int(height/2), :]
    top = pipe(
        trans(lambda img: cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV)[1]),
        trans(lambda img: cv2.erode(img, np.ones((5, 5), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
    )(top)
    fourPoint = getNumberImgFourPoint(top)
    rgb = four_point_transform(lcd_origin, fourPoint)
    threshold = four_point_transform(top, fourPoint)
    return [rgb, threshold]

def getDownNum(lcd_origin, lcd_pre):
    height = lcd_pre.shape[0]
    down = lcd_pre[int(height/2):-1, :]
    down = pipe(
        trans(lambda img: cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV)[1]),
        trans(lambda img: cv2.morphologyEx(img, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))),
        trans(lambda img: cv2.erode(img, np.ones((5, 5), np.uint8))),
    )(down)
    fourPoint = getNumberImgFourPoint(down)
    rgb = four_point_transform(lcd_origin, np.array([[point[0], point[1] + int(height/2)] for point in fourPoint]))
    threshold = four_point_transform(down, fourPoint)
    return [rgb, threshold]

def getLCDNum(img):
    # LCD 前處理
    lcd_pre = pipe(
        trans(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)),
        trans(lambda img: cv2.GaussianBlur(img, (5, 5), 0)),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8), iterations = 2)),
        trans(lambda img: sharpen(img, 120)),
    )(img)

    # 收縮壓
    [topRGB, topTH] = getTopNum(img, lcd_pre)
    cv2.imshow('topRGB',  topRGB)
    cv2.imshow('topTH',  topTH)
    contours, hierarchy = cv2.findContours(topTH.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:
        rect = cv2.boundingRect(cont)
        print(rect)
        cv2.imshow('asdsa', cv2.rectangle(topRGB, (3, 9, 13, 61), (0, 0, 255), 2, 8, 0))
        cv2.imshow('asdsa', cv2.rectangle(topRGB, (44, 7, 13, 64), (0, 0, 255), 2, 8, 0))
        cv2.imshow('asdsa', cv2.rectangle(topRGB, (58, 2, 41, 69), (0, 0, 255), 2, 8, 0))
    print('\n')
    # 舒張壓
    [downRGB, downTH] = getDownNum(img, lcd_pre)
    cv2.imshow('downRGB',  downRGB)
    cv2.imshow('downTH',  downTH)
    contours, hierarchy = cv2.findContours(downTH.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:
        rect = cv2.boundingRect(cont)
        print(rect)
        cv2.imshow('asdsabbb', cv2.rectangle(downRGB, rect, (0, 0, 255), 2, 8, 0))
    cv2.waitKey(0)