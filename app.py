import logic as bd
import tempLogic as temp
import numpy as np
import cv2
import json
from flask import Flask, request
from flask_cors import CORS
from pyzbar.pyzbar import decode

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/bdNum", methods=['POST'])
def bdnum():
    # 圖片格式轉換
    file = request.files["imgData"]
    img = file_to_cv2_img(file)
    # 辨識數值
    lcdImg = bd.getLCDImg(img)
    num = bd.getLCDTopNum(lcdImg) + bd.getLCDDownNum(lcdImg)
    # 判斷結果
    if num.find("x") == -1:
        status = 'success'
    else:
        status = 'fail'
    return json.dumps({ 'status': status })

@app.route("/tempNum", methods=['POST'])
def tempnum():
    # 圖片格式轉換
    file = request.files["imgData"]
    img = file_to_cv2_img(file)
    # 辨識數值
    lcdImg = temp.getLCDImg(img)
    num = temp.getLCDNum(lcdImg)
    # 判斷結果
    if num.find("x") == -1:
        status = 'success'
    else:
        status = 'fail'
    return json.dumps({ 'status': status })

@app.route("/bdQR", methods=['POST'])
def bdQR():
    # 圖片格式轉換
    file = request.files["imgData"]
    img = file_to_cv2_img(file)
    # 辨識數值
    try:
        qrcodeImg = bd.getQrcodeImg(img)
        qrcodeData = decode(qrcodeImg)[0].data
        status = 'success'
    except:
        status = 'fail'
    # 判斷結果
    return json.dumps({ 'status': status })

@app.route("/tempQR", methods=['POST'])
def tempQR():
    # 圖片格式轉換
    file = request.files["imgData"]
    img = file_to_cv2_img(file)
    # 辨識數值
    try:
        qrcodeImg = temp.getQrcodeImg(img)
        qrcodeData = decode(qrcodeImg)[0].data
        status = 'success'
    except:
        status = 'fail'
    # 判斷結果
    return json.dumps({ 'status': status })

def file_to_cv2_img(file):
    npimg = np.fromfile(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return img