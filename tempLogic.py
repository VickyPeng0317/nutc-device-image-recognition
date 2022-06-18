
from imutils.perspective import four_point_transform
import imutils
import cv2
import numpy as np
from base import trans, pipe

def getQrcodeImg(image):
    image = imutils.resize(image, height=500)

    # 灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 邊緣檢測
    edged = cv2.Canny(cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1], 50, 200, 255)
   
    # 在邊緣檢測map中取得輪廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 依大小排序輪廓
    cnts = sorted(cnts, key=cv2.contourArea, reverse=False)
    displayCnt = None

    # 讀取所有輪廓
    for c in cnts:
        # 對輪廓進行相似比對
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x = cv2.boundingRect(c)[0]
        y = cv2.boundingRect(c)[1]
        weight = cv2.boundingRect(c)[2]
        hight = cv2.boundingRect(c)[3]
        # 找出有四個頂點的輪廓
        if len(approx) == 4 and weight*hight > 500:
            # cv2.imshow('rectangle', cv2.rectangle(image,(x,y),(x+weight,y+hight),(0,255,0),5))
            # cv2.imwrite(f'paper/qr/rectangle.png', cv2.rectangle(image,(x,y),(x+weight,y+hight),(0,255,0),5))
            displayCnt = approx
    # 把圖切出來
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))

    return warped

def getLCDImg(image):
    image = imutils.resize(image, height=500)

    # 灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 邊緣檢測
    edged = cv2.Canny(gray, 50, 200, 255)
   
    # 在邊緣檢測map中取得輪廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 依大小排序輪廓
    cnts = sorted(cnts, key=cv2.contourArea, reverse=False)
    displayCnt = None

    # 讀取所有輪廓
    for c in cnts:
        # 對輪廓進行相似比對
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        weight = cv2.boundingRect(c)[2]
        hight = cv2.boundingRect(c)[2]
        # 找出有四個頂點的輪廓
        if len(approx) == 4 and weight*hight > 20000:
            displayCnt = approx
       
    
    # 把圖切出來
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))

    return warped

def getLCDNum(lcd_img):
    alter_lcd_img = pipe(
        trans(lambda img: cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        # trans(lambda img: cv2.dilate(img, np.ones((2, 2), np.uint8))),
        # tap(lambda img: cv2.imshow('getDownImg', img)),
    )(lcd_img)
    topNumImgArr = getNumImgArr(alter_lcd_img, lcd_img, D = 40)
    # i = 0
    # for a in topNumImgArr:
    #     cv2.imshow(f'qq{i}', a)
    #     i = i + 1
    # print(topNumImgArr[2].shape)
    topAllNumber = [sevenDisplayNum(numImg) for numImg in topNumImgArr]
    # print(f'{topAllNumber[0]}{topAllNumber[1]}.{topAllNumber[2]}')
    return f'{topAllNumber[0]}{topAllNumber[1]}.{topAllNumber[2]}'

def getLCDNumImgArr(lcd_img):
    alter_lcd_img = pipe(
        trans(lambda img: cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        # trans(lambda img: cv2.dilate(img, np.ones((2, 2), np.uint8))),
        # tap(lambda img: cv2.imshow('getDownImg', img)),
    )(lcd_img)
    numImgArr = getNumImgArr(alter_lcd_img, lcd_img, D = 40)
    return numImgArr

def getNumImgArr(thImg, rgbImg, D = 10):
    # 找出 boundingRect 並依 X 座標值由小排到大
    contours, hierarchy = cv2.findContours(thImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boundingRectArr = np.array([cv2.boundingRect(c) for c in contours])
    boundingMean = (sum([r[2] * r[3] for r in boundingRectArr])/len(boundingRectArr))*0.75
    boundingRectArr = np.array(list(filter(lambda rect: (rect[2] * rect[3]) > boundingMean, boundingRectArr)))
    boundingRectArr = boundingRectArr[boundingRectArr[:, 0].argsort()]
    # boundingRectArr = boundingRectArr[np.where((boundingRectArr[:, 2]*boundingRectArr[:, 3]) > 50)]
    # 於 Index 0 新增 isSelect flag 值
    boundingRectLogicArr = np.array([[0, *rect] for rect in boundingRectArr])

    # print('')
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
        www = rect[2]
        # 找出鄰近 rect index， D為區間值
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
        # print(item)
        # print(fourPoint)
        # 忽略過小
        if (endX-startX) * (endY-startY) > 500:
            # cv2.imshow(f'Rect{2}', cv2.rectangle(rgbImg,(startX,startY),(endX,endY),(0,255,0),2))
            boundingRectFourPoint.append(fourPoint)
    # 回傳數字圖像
    return [four_point_transform(thImg, fourPoint) for fourPoint in boundingRectFourPoint]

def getNumberImgFourPoint(img, orgin):
    # 找出輪廓
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 取得外接矩形
    boundingRectArr = np.array([cv2.boundingRect(c) for c in contours])
    print(boundingRectArr)
    # i = 1
    # for rect in boundingRectArr:
    #     x,y,w,h = rect
    #     cv2.imshow(f'Rect{1}', cv2.rectangle(orgin,(x,y),(x+w,y+h),(0,255,0),2))

    # 取得最左上方座標
    [startX, startY, *_] = np.amin(boundingRectArr, axis=0)

    # 取得最右下方座標
    boundingRectEndPointArr = [[ar[0] + ar[2], ar[1] + ar[3]] for ar in boundingRectArr]
    [endX, endY, *_] = np.amax(boundingRectEndPointArr, axis=0)

    # 組出外接矩形4個座標， D 為矩形外擴閥值
    D = 1
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
    # cv2.imshow(f'Rectasdas', cv2.rectangle(orgin,(startX,startY),(endX,endY),(0,255,0),2))
    return fourPoint

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
        # cv2.imshow(f'Rect{2}', cv2.rectangle(img,(xA,yA),(xB,xB),(0,255,0),2))
        # 如果非零区域的个数大于整个区域的一半，则认为该段是亮的
        matchPersent = 0.3
        # 右下比較細，需調低
        if i == 5:
            matchPersent = 0.25
        if total / float(area) > matchPersent:
            on[i]= 1
    # # 进行数字查询并显示结果
    try:
        # print(on)
        digit = DIGITS_LOOKUP[tuple(on)]
    except:
        # print(on)
        digit = 'x'
    return str(digit)