import cv2
import pandas as pd
import numpy as np
import copy

CCS_LAB_A_MIN=-70
CCS_LAB_A_MAX=80
CCS_LAB_B_MIN=-70
CCS_LAB_B_MAX=100



#http://www.easyrgb.com/en/math.php
def labTorgb(labData):

    CIE_L = labData[0]
    CIE_a = labData[1]
    CIE_b = labData[2]
    #LAB -> XYZ
    var_Y = (CIE_L  + 16.) / 116.
    var_X = CIE_a  / 500. + var_Y
    var_Z = var_Y - CIE_b  / 200.

    if (var_Y ** 3 > 0.008856) : var_Y = var_Y ** 3
    else                       : var_Y = ( var_Y - 16 / 116 ) / 7.787
    if (var_X ** 3 > 0.008856) :var_X = var_X ** 3
    else                      : var_X = ( var_X - 16 / 116 ) / 7.787
    if (var_Z ** 3 > 0.008856): var_Z = var_Z ** 3
    else                      : var_Z = ( var_Z - 16 / 116 ) / 7.787

    X = var_X * 95.047   #Reference - X
    Y = var_Y * 100.     #Reference - Y
    Z = var_Z * 108.883  #Reference - Z
    
    #print X,Y,Z

    # XYZ -> RGB
    var_X = X / 100
    var_Y = Y / 100
    var_Z = Z / 100

    var_R = var_X * 3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y * 1.8758 + var_Z * 0.0415
    var_B = var_X * 0.0557 + var_Y * -0.2040 + var_Z * 1.0570

    if (var_R > 0.0031308) : var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
    else                   : var_R = 12.92 * var_R
    if (var_G > 0.0031308) : var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
    else                   : var_G = 12.92 * var_G
    if (var_B > 0.0031308) : var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
    else                   : var_B = 12.92 * var_B

    if (var_R < 0.):
        var_R = 0.
    if (var_R > 1.):
        var_R = 1.

    if (var_G < 0.):
        var_G = 0.
    if (var_G > 1.):
        var_G = 1.

    if (var_B < 0.):
        var_B = 0.
    if (var_B > 1.):
        var_B = 1.

    sR = var_R * 255
    sG = var_G * 255
    sB = var_B * 255

    cdRGB = np.zeros(3, np.uint8)
    cdRGB[2] = sR
    cdRGB[1] = sG
    cdRGB[0] = sB
    #print cdRGB
    return cdRGB

def rgbTolab(labData):
    return

width =CCS_LAB_A_MAX-CCS_LAB_A_MIN
height =CCS_LAB_B_MAX-CCS_LAB_B_MIN

cv2.namedWindow('Lab', flags =cv2.WINDOW_NORMAL  )
imgLabOrg = np.zeros((height,width,3), np.uint8)
imgLabOut = np.zeros((height, width, 3), np.uint8)

cdLAB = np.zeros(3, np.float)
cdLAB[0] = 90.

for b in range(CCS_LAB_B_MIN, CCS_LAB_B_MAX):
    for a in range(CCS_LAB_A_MIN, CCS_LAB_A_MAX):
        cdLAB[1] = a
        cdLAB[2] = b

        y = height - (abs(CCS_LAB_B_MIN) + b) - 1
        x = abs(CCS_LAB_A_MIN)+a
        imgLabOrg[y,x] = labTorgb(cdLAB)



imgLabOrg = cv2.resize(imgLabOrg, (width*2, height*2), interpolation=cv2.INTER_CUBIC)




def DrowABPos(IdealRGB,ReadRGB):
    global imgLabOut
    #ReadTmp = np.zeros((4, 6, 3), np.int)
    LABtmp = np.zeros(3, np.float)
    LABtmp = rgbTolab(IdealRGB)

    return

def ShowLabRect():
    global imgLabOrg,imgLabOut
    imgLabOut = copy.deepcopy(imgLabOrg)
    DrowABPos()
    cv2.imshow('Lab', imgLabOut)
    return