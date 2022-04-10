from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

def getQrcode(image):
    # resize 500
    image = imutils.resize(image, height=500)
    # 灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('output/1-cvtColor.png', gray)
    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite('output/2-GaussianBlur.png', blurred)
    # 邊緣檢測
    edged = cv2.Canny(blurred, 50, 200, 255)
    cv2.imwrite('output/3-Canny.png', edged)
    
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
    cv2.imwrite('output/origin-qrcode.png', warped)

    # 二值化
    thresh = cv2.threshold(warped, 100, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('output/threshold-qrcode.png', thresh)
    return thresh