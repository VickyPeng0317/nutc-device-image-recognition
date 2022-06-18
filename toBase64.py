import base64
import cv2

# bdQRSuccess = 1
# bdQRSuccess_as_text = base64.b64encode(cv2.imread(f"img/{str(bdQRSuccess)}.png"))
# with open('test/bdQRSuccess.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{bdQRSuccess_as_text.decode("utf-8")}')

# bdQRFail = 4
# bdQRFail_as_text = base64.b64encode(cv2.imread(f"img/{str(bdQRFail)}.png"))
# with open('test/bdQRFail.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{bdQRFail_as_text.decode("utf-8")}')

# tempQRSuccess = 1
# tempQRSuccess_as_text = base64.b64encode(cv2.imread(f"img2/{str(tempQRSuccess)}.jpg"))
# with open('test/tempQRSuccess.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{tempQRSuccess_as_text.decode("utf-8")}')

# tempQRFail = 8
# tempQRFail_as_text = base64.b64encode(cv2.imread(f"img2/{str(tempQRFail)}.jpg"))
# with open('test/tempQRFail.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{tempQRFail_as_text.decode("utf-8")}')


# #################

# bdNumberSuccess = 1
# bdNumberSuccess_as_text = base64.b64encode(cv2.imread(f"img/{str(bdNumberSuccess)}.png"))
# with open('test/bdNumberSuccess.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{bdNumberSuccess_as_text.decode("utf-8")}')

# bdNumberFail = 33
# bdNumberFail_as_text = base64.b64encode(cv2.imread(f"img/{str(bdNumberFail)}.png"))
# with open('test/bdNumberFail.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{bdNumberFail_as_text.decode("utf-8")}')

# tempNumberSuccess = 1
# tempNumberSuccess_as_text = base64.b64encode(cv2.imread(f"img2/{str(tempNumberSuccess)}.jpg"))
# with open('test/tempNumberSuccess.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{tempNumberSuccess_as_text.decode("utf-8")}')

# tempNumberFail = 6
# tempNumberFail_as_text = base64.b64encode(cv2.imread(f"img2/{str(tempNumberFail)}.jpg"))
# with open('test/tempNumberFail.txt', 'w') as f:
#     f.write(f'data: image/png;base64,{tempNumberFail_as_text.decode("utf-8")}')



bdQRSuccess = 1
cv2.imwrite('test/bdQRSuccess.png', cv2.imread(f"img/{str(bdQRSuccess)}.png"))


bdQRFail = 4
cv2.imwrite('test/bdQRFail.png', cv2.imread(f"img/{str(bdQRFail)}.png"))

tempQRSuccess = 1
cv2.imwrite('test/tempQRSuccess.jpg', cv2.imread(f"img2/{str(tempQRSuccess)}.jpg"))

tempQRFail = 8
cv2.imwrite('test/tempQRFail.jpg', cv2.imread(f"img2/{str(tempQRFail)}.jpg"))


#################

bdNumberSuccess = 1
cv2.imwrite('test/bdNumberSuccess.png', cv2.imread(f"img/{str(bdNumberSuccess)}.png"))

bdNumberFail = 33
cv2.imwrite('test/bdNumberFail.png', cv2.imread(f"img/{str(bdNumberFail)}.png"))

tempNumberSuccess = 1
cv2.imwrite('test/tempNumberSuccess.jpg', cv2.imread(f"img2/{str(tempNumberSuccess)}.jpg"))

tempNumberFail = 6
cv2.imwrite('test/tempNumberFail.jpg', cv2.imread(f"img2/{str(tempNumberFail)}.jpg"))

