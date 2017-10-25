import cv2
import pandas as pd
import numpy as np
import copy

"""
filename =  filedialog.askopenfilename()
if len(filename) is 0:
    exit()
print filename
img_Org = cv2.imread( filename, cv2.COLOR_BGR2RGB )
"""

img_Org = cv2.imread( "In.bmp", cv2.COLOR_BGR2RGB )
jpgheight, jpgwidth, jpgch = img_Org.shape

img = np.zeros(img_Org.shape, np.int)
imgOut = np.zeros(img_Org.shape, np.int)
imgOut = copy.deepcopy(img_Org)


drawing = 0
RectOutBoxPos = np.zeros((3,3,2), np.int)


tglBoxSize=4

def draw_RectOut():
    global img,RectOutBoxPos
    ix = RectOutBoxPos[0][0][0]
    iy = RectOutBoxPos[0][0][1]
    x =  RectOutBoxPos[2][2][0]
    y = RectOutBoxPos[2][2][1]
    midsizeX = (x - ix) / 2
    midsizeY = (y - iy) / 2

    RectOutBoxPos[0][1][1] = RectOutBoxPos[0][0][1]



    #cv2.rectangle(img, (ix, iy), (x, y), (255, 255, 255), 1)
    cv2.line(img, (ix, iy), (ix+midsizeX, iy), (255, 255, 255), 1)
    cv2.line(img, (ix + midsizeX, iy),(x , iy), (255, 255, 255), 1)

    cv2.line(img, (ix, y), (ix + midsizeX, y), (255, 255, 255), 1)
    cv2.line(img, (ix + midsizeX, y), (x, y), (255, 255, 255), 1)

    cv2.line(img, (ix, iy), (ix , iy+ midsizeY), (255, 255, 255), 1)
    cv2.line(img, (ix, iy + midsizeY),(ix, y), (255, 255, 255), 1)

    cv2.line(img, (x, iy), (x, iy + midsizeY), (255, 255, 255), 1)
    cv2.line(img, (x, iy + midsizeY), (x, y), (255, 255, 255), 1)


    cv2.rectangle(img, (ix - tglBoxSize, iy - tglBoxSize), (ix + tglBoxSize, iy + tglBoxSize), (255, 255, 255), 1)
    cv2.rectangle(img, (ix - tglBoxSize, y - tglBoxSize), (ix + tglBoxSize, y + tglBoxSize), (255, 255, 255), 1)
    cv2.rectangle(img, (x - tglBoxSize, iy - tglBoxSize), (x + tglBoxSize, iy + tglBoxSize), (255, 255, 255), 1)
    cv2.rectangle(img, (x - tglBoxSize, y - tglBoxSize), (x + tglBoxSize, y + tglBoxSize), (255, 255, 255), 1)

    cv2.rectangle(img, (ix + midsizeX - tglBoxSize, iy - tglBoxSize), (ix + midsizeX + tglBoxSize, iy + tglBoxSize),
                  (255, 255, 255), 1)
    cv2.rectangle(img, (ix + midsizeX - tglBoxSize, y - tglBoxSize), (ix + midsizeX + tglBoxSize, y + tglBoxSize),
                  (255, 255, 255), 1)
    cv2.rectangle(img, (ix - tglBoxSize, iy + midsizeY - tglBoxSize), (ix + tglBoxSize, iy + midsizeY + tglBoxSize),
                  (255, 255, 255), 1)
    cv2.rectangle(img, (x - tglBoxSize, iy + midsizeY - tglBoxSize), (x + tglBoxSize, iy + midsizeY + tglBoxSize),
                  (255, 255, 255), 1)

def Check_RectOutBoxIn(x,y):
    return 0

def draw_circle(event, x,y, flags, param):
    global drawing, img, img_Org, imgOut,RectOutBoxPos

    if event == cv2.EVENT_LBUTTONDOWN:
        if Check_RectOutBoxIn(x,y) ==0:
            drawing = 1
            RectOutBoxPos[0][0][0] = x
            RectOutBoxPos[0][0][1] = y


    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == 1:
           img = np.zeros(img_Org.shape, np.int)
           img = copy.deepcopy(img_Org)
           cv2.rectangle(img,(RectOutBoxPosXStart,RectOutBoxPosYStart),(x,y),(255,0,0),1)
           imgOut = copy.deepcopy(img)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == 1:
            RectOutBoxPos[2][2][0] = x
            RectOutBoxPos[2][2][1] = y
            drawing = 2
            img = np.zeros(img_Org.shape, np.int)
            img = copy.deepcopy(img_Org)
            draw_RectOut()
            imgOut = copy.deepcopy(img)




cv2.namedWindow('imgOut')
cv2.setMouseCallback('imgOut',draw_circle)

#cv2.rectangle(img, (195, 105), (514, 364),(255,255,255),1)

while True:
    cv2.imshow('imgOut', imgOut)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()
