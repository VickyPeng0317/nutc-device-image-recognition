from ast import Lambda
from re import X
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
from base import trans, tap, pipe
from lib import sharpen, modify_contrast_and_brightness2
from matplotlib import pyplot as plt

def getQrcodeImg(image):
    # cv2.imshow('image', image)
    # resize 500
    # image = imutils.resize(image, height=500)
    height = image.shape[0]
    image = image[int(height/2):-1, :]

    # cv2.imshow('1', image)

    # 灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('2', gray)

    # 邊緣檢測
    edged = cv2.Canny(gray, 50, 200, 255)
    # cv2.imshow('3', edged)

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
        if len(approx) == 4 and weight > 30:
            displayCnt = approx
            break
    
    # 把圖切出來
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    # cv2.imshow('4', warped)
    # cv2.imwrite('output/QR/origin-qrcode.png', warped)
    # 銳化
    # blur_img = cv2.GaussianBlur(warped, (0, 0), 150)
    # usm = cv2.addWeighted(warped, 1.5, blur_img, -0.5, 0)

    # hist = np.array(cv2.calcHist([warped],[0],None,[256],[0,256]))
    # #Convert histogram to simple list
    # hist = [val[0] for val in hist]

    # #Generate a list of indices
    # indices = list(range(0, 256))

    # #Descending sort-by-key with histogram value as key
    # s = [(x,y) for y,x in sorted(zip(hist,indices), reverse=True)]

    # #Index of highest peak in histogram
    # index_of_highest_peak = s[0][0]

    # #Index of second highest peak in histogram
    # index_of_second_highest_peak = s[1][0]

    # midpoint = int( (index_of_highest_peak + index_of_second_highest_peak) / 2.0 )
        


    # plt.figure()#新建一個影象
    # plt.title("Grayscale Histogram")
    # plt.xlabel("Bins") #X軸標籤
    # plt.ylabel("# of Pixels") #Y軸標籤
    # plt.plot(hist)
    # plt.xlim([0,256]) #設定x座標軸範圍
    # plt.show()

    # print(int(mean))
    # return cv2.threshold(warped, hist[midpoint]*0.75, 255, cv2.THRESH_BINARY)[1]
    return cv2.threshold(warped, 175, 255, cv2.THRESH_BINARY)[1]
    #return warped

def getLCDImg(image):
    (B, R, G) = cv2.split(image)
    # cv2.imshow('B', B)
    # cv2.imshow('R', R)
    # cv2.imshow('G', G)
    # cv2.imwrite('output/getNumber/ORIGIN.png', image)
    # cv2.imwrite('output/getNumber/B.png', B)
    # cv2.imwrite('output/getNumber/R.png', R)
    # cv2.imwrite('output/getNumber/G.png', G)
    # 高斯模糊
    # blurred = cv2.GaussianBlur(B, (3, 3), 0)
    # cv2.imshow('2', blurred)
    # cv2.imwrite('output/getNumber/B_1-blurred.png', blurred)
    # 邊緣檢測
    edged = cv2.Canny(B, 50, 200, 255)
    # cv2.imshow('2', edged)
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
    # cv2.imshow('lcd', lcdAreaImg)
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

def getNumberImgFourPoint(img, orgin):
    # 找出輪廓
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 取得外接矩形
    boundingRectArr = np.array([cv2.boundingRect(c) for c in contours])

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
    # cv2.imshow(f'Rectasdas', cv2.rectangle(orgin,(startX,startY),(endX,endY),(0,255,0),2))
    return fourPoint

def getTopImg(lcd_origin):
    lcd_origin_top = lcd_origin[0:int(lcd_origin.shape[0]/2), :]
    orgin_top = lcd_origin_top[int(lcd_origin_top.shape[0]/3):-1, :]
    # cv2.imshow('origin', orgin_top)
    top = pipe(
        # trans(lambda img: cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV)[1]),
        trans(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)),
        # tap(lambda img: cv2.imshow('G', img)),
        trans(lambda img: cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)[1]),
        # tap(lambda img: cv2.imshow('B', img)),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.erode(img, np.ones((3, 3), np.uint8))),
        trans(lambda img: cv2.dilate(img, np.ones((3, 3), np.uint8))),
        # tap(lambda img: cv2.imshow('A', img)),
    )(orgin_top)
    # cv2.imshow('canny', cv2.Canny(top, 50, 200, 255))
    fourPoint = getNumberImgFourPoint(top, orgin_top)
    rgb = four_point_transform(orgin_top, fourPoint)
    threshold = four_point_transform(top, fourPoint)
    # cv2.imshow('threshold', threshold)
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
    fourPoint = getNumberImgFourPoint(down, orgin_down)
    rgb = four_point_transform(orgin_down, fourPoint)
    threshold = four_point_transform(down, fourPoint)
    return [rgb, threshold]

def getNumImgArr(thImg, rgbImg, D = 10):
    # 找出 boundingRect 並依 X 座標值由小排到大
    contours, hierarchy = cv2.findContours(thImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boundingRectArr = np.array([cv2.boundingRect(c) for c in contours])

    # i = 1
    # for rect in boundingRectArr:
    #     x,y,w,h = rect
    #     cv2.imshow(f'Rect{1}', cv2.rectangle(rgbImg,(x,y),(x+w,y+h),(0,255,0),2))

    boundingRectArr = boundingRectArr[boundingRectArr[:, 0].argsort()]
    boundingRectArr = boundingRectArr[np.where((boundingRectArr[:, 2]*boundingRectArr[:, 3]) > 50)]

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
        # print(www)
        groupIndex = np.where((boundingRectLogicArr[:, 1] >= startX) & (boundingRectLogicArr[:, 1] <= (startX+(www*0.8))))[0]
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
        if (endX-startX) * (endY-startY) > 300:
            # cv2.imshow(f'Rect{2}', cv2.rectangle(rgbImg,(startX,startY),(endX,endY),(0,255,0),2))
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
        # cv2.imshow(f'Rect{2}', cv2.rectangle(img,(xA,yA),(xB,xB),(0,255,0),2))
        # 如果非零区域的个数大于整个区域的一半，则认为该段是亮的
        matchPersent = 0.4
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

def getLCDTopNum(lcd_img):
    # 收縮壓
    [topRGB, topTH] = getTopImg(lcd_img)
    topNumImgArr = getNumImgArr(topTH, topRGB, D = 10)
    # for i in range(len(topNumImgArr)):
    #     cv2.imwrite(f'output/TOPNum-{i+1}.png', topNumImgArr[i])
    topAllNumber = [sevenDisplayNum(numImg) for numImg in topNumImgArr]
    return "".join(topAllNumber)

def getLCDDownNum(lcd_img):
    # 舒張壓
    [downRGB, downTH] = getDownImg(lcd_img)
    downNumImgArr = getNumImgArr(downTH, downRGB, D = 20)
    # for i in range(len(downNumImgArr)):
    #     cv2.imshow(f'Num-{i+1}', downNumImgArr[i])
    downAllNumber = [sevenDisplayNum(numImg) for numImg in downNumImgArr]
    return "".join(downAllNumber)
    # # cv2.imshow(f'testasdsa', downNumImgArr[0])
    # return sevenDisplayNum(downNumImgArr[0])

def getLCDTopNumImgArr(lcd_img):
    # 收縮壓
    [topRGB, topTH] = getTopImg(lcd_img)
    topNumImgArr = getNumImgArr(topTH, topRGB, D = 10)
    return topNumImgArr

def getLCDDownNumImgArr(lcd_img):
    # 舒張壓
    [downRGB, downTH] = getDownImg(lcd_img)
    downNumImgArr = getNumImgArr(downTH, downRGB, D = 20)
    return downNumImgArr