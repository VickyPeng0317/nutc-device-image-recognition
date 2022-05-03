from ast import Lambda
from re import X
from cv2 import imshow
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
from base import trans, tap, pipe
from lib import sharpen, modify_contrast_and_brightness2

def getQrcodeImg(image):
    # cv2.imshow('image', image)
    # resize 500
    image = imutils.resize(image, height=500)
    height = image.shape[0]
    image = image[int(height/2):-1, :]

    cv2.imshow('1', image)

    # 灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow('2', gray)

    # 邊緣檢測
    edged = cv2.Canny(cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1], 50, 200, 255)
    cv2.imshow('3', edged)
    cv2.imshow('4', cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1])
    # 在邊緣檢測map中取得輪廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 依大小排序輪廓
    cnts = sorted(cnts, key=cv2.contourArea, reverse=False)
    displayCnt = None
    print(len(cnts))
    # 讀取所有輪廓
    i = 99
    for c in cnts:
        # 對輪廓進行相似比對
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        weight = cv2.boundingRect(c)[2]
        hight = cv2.boundingRect(c)[2]
        x = cv2.boundingRect(c)[0]

        # 找出有四個頂點的輪廓
        # if len(approx) == 4 and weight*hight > 500:
        #     displayCnt = approx
        displayCnt = approx
        print(f'{str(i)} {cv2.boundingRect(c)}')
        try:
            cv2.imshow(f'{str(i)}pic', four_point_transform(gray, displayCnt.reshape(4, 2)))
        except:
            print(f'{str(i)} fail')
       
    
    # 把圖切出來
    # warped = four_point_transform(gray, displayCnt.reshape(4, 2))

    # data= warped.reshape(1, warped.shape[0] * warped.shape[1])[0]
    # mean = sum(data)/len(data)

    return edged