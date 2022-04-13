from ast import Lambda
from re import X
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np

def pipe(*funcs):
    def execute(data):
        result = data
        for i in range(0, len(funcs)):
            result = funcs[i](result)
        cv2.waitKey(0)
        return result
    return execute

def sharpen(img, sigma=100):    
    # https://www.wongwonggoods.com/python/python_opencv/opencv-sharpen-images/
    # sigma = 5、15、25
    blur_img = cv2.GaussianBlur(img, (0, 0), sigma)
    usm = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)
    return usm

def modify_contrast_and_brightness2(img, brightness=0 , contrast=100):
    # 上面做法的問題：有做到對比增強，白的的確更白了。
    # 但沒有實現「黑的更黑」的效果
    import math
    
    brightness = 0
    # contrast = -100 # - 減少對比度/+ 增加對比度

    B = brightness / 255.0
    c = contrast / 255.0 
    k = math.tan((45 + 44 * c) / 180 * math.pi)

    img = (img - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
      
    # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
    img = np.clip(img, 0, 255).astype(np.uint8)
    return img


def getQrcode(image):
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
    return thresh

def getNumber(image):
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
    # for c in arr:
    #     # 把圖切出來
    #     warped = four_point_transform(R, c.reshape(4, 2))
    #     cv2.imwrite(f'output/getNumber/contourArea/{i}.png', warped)
    #     print(cv2.contourArea(arr[i]))
    #     i = i + 1
        # # 二值化
        # thresh = cv2.threshold(warped, 100, 255, cv2.THRESH_BINARY)[1]
        # cv2.imwrite('output/QR/threshold-qrcode.png', thresh)
    getLCDNum2(lcdAreaImg)

def getLCDNum(img):
    (x, y, z) = img.shape
    # SBPImg = img[0:int(x/2),:,:]
    # cv2.imwrite('output/LCD/TEST.png', )
    # cv2.imwrite('output/LCD/TEST2.png', img[int(x/2):-1,:,:])
    # 灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('output/LCD/gray.png', gray)
    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite('output/LCD/GaussianBlur.png', blurred)
    # 侵蝕
    erodedKernel = np.ones((3, 3), np.uint8) 
    eroded = cv2.erode(blurred, erodedKernel, iterations = 2)
    cv2.imwrite('output/LCD/erode.png', eroded)
    # 膨脹
    dilatedKernel = np.ones((7, 7), np.uint8)
    dilated = cv2.dilate(eroded, dilatedKernel)
    cv2.imwrite('output/LCD/dilated.png', dilated)
    # 高斯模糊
    blurred = cv2.GaussianBlur(dilated, (5, 5), 0)
    cv2.imwrite('output/LCD/dilated-GaussianBlur.png', blurred)
    # 侵蝕
    erodedKernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(blurred, erodedKernel)
    cv2.imwrite('output/LCD/eroded-2.png', eroded)
    # 銳化
    sharpened = sharpen(eroded, 120)
    cv2.imwrite('output/LCD/TEST.png', sharpened)
    # 二值
    TOP = cv2.threshold(sharpened[0:int(x/2),:], 35, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite('output/LCD/TOP.png', TOP)
    DOWN = cv2.threshold(sharpened[int(x/2):-1,:], 25, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite('output/LCD/DOWN.png', DOWN)
    # print(thresh.shape)
    # cnts = cv2.findContours(TOP.copy(), cv2.RETR_EXTERNAL,
    #     cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # digitCnts = []
    # print(cnts[0])
    # # loop over the digit area candidates
    # for c in cnts:
    #     # compute the bounding box of the contour
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     # if the contour is sufficiently large, it must be a digit
    #     if (h <= 70 and h >= 50):
    #         digitCnts.append(c)
    # print(len(digitCnts))
    # # 型態
    # morphologyExKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 2))
    # morphologyEx = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, morphologyExKernel)
    # cv2.imwrite('output/LCD/TEST.png', morphologyEx)


def tap(func):
    def resFunc(data):
        func(data)
        return data
    return resFunc    


def getLCDNum2(img):
    pipe(
        lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
        lambda img: cv2.GaussianBlur(img, (5, 5), 0),
        lambda img: cv2.erode(img, np.ones((3, 3), np.uint8), iterations = 2),
        # lambda img: cv2.dilate(img, np.ones((7, 7), np.uint8)),
        # lambda img: cv2.GaussianBlur(img, (5, 5), 0),
        # lambda img: cv2.erode(img, np.ones((5, 5), np.uint8)),
        lambda img: sharpen(img, 120),
        lambda img: cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV)[1],
        tap(lambda img: cv2.imshow('final', img)),
    )(img)
    