from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np

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
    cv2.imwrite('output/getNumber/R_1-blurred.png', blurred)
    # 邊緣檢測
    edged = cv2.Canny(blurred, 50, 200, 255)
    cv2.imwrite('output/getNumber/R_2-Canny.png', edged)

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
    lcdAreaImg = four_point_transform(R, allApprox[lcdAreaIndex].reshape(4, 2))
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
