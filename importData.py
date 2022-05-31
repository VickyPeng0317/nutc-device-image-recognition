import os
import cv2
sourcefolderPath = './img2/2'
importTo = './img2'
seqNo = 21
for fileName in os.listdir(sourcefolderPath):
    file = cv2.imread(f"{sourcefolderPath}/{fileName}")
    cv2.imwrite(f'{importTo}/{seqNo}.jpg', file)
    seqNo = seqNo + 1