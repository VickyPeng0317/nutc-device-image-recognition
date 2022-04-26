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
    height = image.shape[0]
    image = image[int(height/2):-1, :]

    # 灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 邊緣檢測
    edged = cv2.Canny(gray, 50, 200, 255)

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
        weight = cv2.boundingRect(c)[2]

        # 找出有四個頂點的輪廓
        if len(approx) == 4 and weight > 80:
            displayCnt = approx
            break
    
    # 把圖切出來
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    cv2.imwrite('output/QR/origin-qrcode.png', warped)
    # 銳化
    blur_img = cv2.GaussianBlur(warped, (0, 0), 150)
    usm = cv2.addWeighted(warped, 1.5, blur_img, -0.5, 0)

    return usm

def getLCDImg(image):
    (B, R, G) = cv2.split(image)
    # cv2.imwrite('output/getNumber/ORIGIN.png', image)
    # cv2.imwrite('output/getNumber/B.png', B)
    # cv2.imwrite('output/getNumber/R.png', R)
    # cv2.imwrite('output/getNumber/G.png', G)
    # 高斯模糊
    blurred = cv2.GaussianBlur(B, (3, 3), 0)
    # cv2.imwrite('output/getNumber/B_1-blurred.png', blurred)
    # 邊緣檢測
    edged = cv2.Canny(blurred, 50, 200, 255)
    # cv2.imwrite('output/getNumber/B_2-Canny.png', edged)

    # 在邊緣檢測map中取得輪廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 依大小排序輪廓
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    transRect = None
    # 讀取所有輪廓
    for c in cnts:
        # 取得外接四邊形資訊
        x = cv2.boundingRect(c)[0]
        weight = cv2.boundingRect(c)[2]
        height = cv2.boundingRect(c)[3]
        
        # 符合 LCD 大小
        if (weight > 150 and weight < 250) and (height > 150 and height < 250) and (x > 150 and x < 300):
            transRect = cv2.boundingRect(c)

    # 切割 LCD 區塊
    lcdAreaImg = four_point_transform(image, boundingRectToFourPoint(transRect))
    return lcdAreaImg


def boundingRectToFourPoint(rect, D = 1):
    x, y, w, h = rect
    startX = int(x / D)
    startY = int(y / D)
    endX = int((x + w) * D)
    endY = int((y + h) * D)
    fourPoint = np.array([
        [startX, startY],
        [startX, endY],
        [endX, endY],
        [endX, startY],
    ])
    return fourPoint

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

def getTopImg(lcd_origin):
    lcd_origin_top = lcd_origin[0:int(lcd_origin.shape[0]/2), :]
    orgin_top = lcd_origin_top[int(lcd_origin_top.shape[0]/3):-1, :]
    top = pipe(
        # trans(lambda img: cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV)[1]),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)),
        trans(lambda img: cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)[1]),
    )(orgin_top)
    fourPoint = getNumberImgFourPoint(top)
    rgb = four_point_transform(orgin_top, fourPoint)
    threshold = four_point_transform(top, fourPoint)
    return [rgb, threshold]

def getDownImg(lcd_origin):
    lcd_origin_down = lcd_origin[int(lcd_origin.shape[0]/2):-1, :]
    orgin_down = lcd_origin_down[0:int(lcd_origin_down.shape[0]*2/3), :]
    down = pipe(
        # tap(lambda img: cv2.imshow('getDownImg', img)),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)),
        trans(lambda img: cv2.GaussianBlur(img, (5, 5), 150)),
        trans(lambda img: cv2.threshold(img, 35, 255, cv2.THRESH_BINARY_INV)[1]),
        # trans(lambda img: cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV)[1]),
        # trans(lambda img: cv2.morphologyEx(img, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))),
        # trans(lambda img: cv2.erode(img, np.ones((5, 5), np.uint8))),
    )(orgin_down)
    fourPoint = getNumberImgFourPoint(down)
    rgb = four_point_transform(orgin_down, fourPoint)
    threshold = four_point_transform(down, fourPoint)
    return [rgb, threshold]

def getNumImgArr(thImg):
    # 找出 boundingRect 並依 X 座標值由小排到大
    contours, hierarchy = cv2.findContours(thImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boundingRectArr = np.array([cv2.boundingRect(c) for c in contours])
    boundingRectArr = boundingRectArr[boundingRectArr[:, 0].argsort()]
    # 於 Index 0 新增 isSelect flag 值
    boundingRectLogicArr = np.array([[0, *rect] for rect in boundingRectArr])
    # 找出鄰近 boundingRect
    boundingRectGroup = []
    for item in boundingRectLogicArr:
        # 取值
        [isSelect, *rect] = item
        # 已被挑選就離開
        if isSelect == 1:
            continue
        # 取得 x 座標
        startX = rect[0]
        # 找出鄰近 rect index， D為區間值
        D = 10
        groupIndex = np.where((boundingRectLogicArr[:, 1] >= startX) & (boundingRectLogicArr[:, 1] <= (startX+D)))[0]
        # 儲存鄰近 rect group 
        boundingRectGroup.append(boundingRectArr[groupIndex])
        # 將已選取的 rect 之 isSelect flag 設為 1
        for index in groupIndex:
            boundingRectLogicArr[index][0] = 1
    # 找出各群組之外接矩形座標
    boundingRectFourPoint = []
    for item in boundingRectGroup:
        # 取得最左上方座標
        [startX, startY, *_] = np.amin(item, axis=0)

        # 取得最右下方座標
        boundingRectEndPointArr = [[ar[0] + ar[2], ar[1] + ar[3]] for ar in item]
        [endX, endY, *_] = np.amax(boundingRectEndPointArr, axis=0)

        # 組出外接矩形4個座標， D 為矩形外擴閥值
        fourPoint = np.array([
            [startX, startY],
            [startX, endY],
            [endX, endY],
            [endX, startY],
        ])
        # 忽略過小
        if (endX-startX) * (endY-startY) > 500:
            boundingRectFourPoint.append(fourPoint)
    # 回傳數字圖像
    return [four_point_transform(thImg, fourPoint) for fourPoint in boundingRectFourPoint]

def sevenDisplayNum(img):
    # 太窄代表是 1
    [h, w] = img.shape
    if (w < 20) :
        return '1'
    # 定義數值陣列
    DIGITS_LOOKUP = {
        (1, 1, 1, 0, 1, 1, 1): 0,
        (0, 0, 1, 0, 0, 1, 0): 1,
        (1, 0, 1, 1, 1, 0, 1): 2,
        (1, 0, 1, 1, 0, 1, 1): 3,
        (0, 1, 1, 1, 0, 1, 0): 4,
        (1, 1, 0, 1, 0, 1, 1): 5,
        (1, 1, 0, 1, 1, 1, 1): 6,
        (1, 0, 1, 0, 0, 1, 0): 7,
        (1, 1, 1, 1, 1, 1, 1): 8,
        (1, 1, 1, 1, 0, 1, 1): 9
    }
    www = int(w * 0.25)
    segments = [
        ((0, 0), (w, www)),               # 上
        ((0, 0), (www, h // 2)),           # 左上
        ((w - www, 0), (w, h // 2)),          # 右上
        ((0, (h // 2) - (www//2)) , (w, (h // 2) + (www//2))), # 中间
        ((0, h // 2), (www, h)),            # 左下
        ((w - www, h // 2), (w, h)),          # 右下
        ((0, h - www), (w, h))              # 下
    ]
    on = [0] * len(segments)
     # 循环遍历数码管中的每一段
    for (i, ((xA, yA), (xB, yB))) in enumerate(segments): # 检测分割后的ROI区域，并统计分割图中的阈值像素点
        segROI = img[yA:yB, xA:xB]
        total = cv2.countNonZero(segROI)
        area = (xB - xA) * (yB - yA)
        # 如果非零区域的个数大于整个区域的一半，则认为该段是亮的
        if total / float(area) > 0.4:
            on[i]= 1
    # # 进行数字查询并显示结果
    try:
        # print(on)
        digit = DIGITS_LOOKUP[tuple(on)]
    except:
        # print(on)
        digit = 'x'
    return str(digit)

def getLCDNum(img):
    # 收縮壓
    [topRGB, topTH] = getTopImg(img)
    topNumImgArr = getNumImgArr(topTH)
    # # for i in range(len(topNumImgArr)):
    # #     cv2.imshow(f'Num-{i+1}', topNumImgArr[i])
    topAllNumber = [sevenDisplayNum(numImg) for numImg in topNumImgArr]
    
    # 舒張壓
    [downRGB, downTH] = getDownImg(img)
    downNumImgArr = getNumImgArr(downTH)
    # for i in range(len(downNumImgArr)):
    #     cv2.imshow(f'Num-{i+1}', downNumImgArr[i])
    downAllNumber = [sevenDisplayNum(numImg) for numImg in downNumImgArr]
    # cv2.waitKey(0)
    return "".join(topAllNumber)



    # return ["".join(topAllNumber)]

