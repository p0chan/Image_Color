import cv2
import pandas as pd
import numpy as np
import copy

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
    
    # XYZ -> RGB
    var_X = X / 100.
    var_Y = Y / 100.
    var_Z = Z / 100.

    var_R = var_X * 3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y * 1.8758 + var_Z * 0.0415
    var_B = var_X * 0.0557 + var_Y * -0.2040 + var_Z * 1.0570

    if (var_R > 0.0031308) : var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
    else                   : var_R = 12.92 * var_R
    if (var_G > 0.0031308) : var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
    else                   : var_G = 12.92 * var_G
    if (var_B > 0.0031308) : var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
    else                   : var_B = 12.92 * var_B

    if (var_R < 0.): var_R = 0.
    if (var_R > 1.): var_R = 1.
    if (var_G < 0.): var_G = 0.
    if (var_G > 1.): var_G = 1.
    if (var_B < 0.): var_B = 0.
    if (var_B > 1.): var_B = 1.

    sR = var_R * 255
    sG = var_G * 255
    sB = var_B * 255

    cdRGB = np.zeros(3, np.uint8)
    cdRGB[2] = sR
    cdRGB[1] = sG
    cdRGB[0] = sB
    #print cdRGB
    return cdRGB

def rgbTolab(RGB):

    sR = RGB[2]
    sG = RGB[1]
    sB = RGB[0]

    var_R = (sR / 255.)
    var_G = (sG / 255.)
    var_B = (sB / 255.)

    if (var_R > 0.04045) :var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else                 :var_R = var_R / 12.92
    if (var_G > 0.04045) :var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else                 :var_G = var_G / 12.92
    if (var_B > 0.04045) :var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else                 :var_B = var_B / 12.92

    var_R = var_R * 100.
    var_G = var_G * 100.
    var_B = var_B * 100.

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    #XYZ ->CIE-L*ab
    var_X = X / 95.047 #Reference - X
    var_Y = Y / 100.   #Reference - Y
    var_Z = Z / 108.883#Reference - Z

    if (var_X > 0.008856) :var_X = var_X ** ( 1. / 3. )
    else                  :var_X = ( 7.787 * var_X ) + ( 16. / 116. )
    if (var_Y > 0.008856) :var_Y = var_Y ** ( 1. / 3. )
    else                  :var_Y = ( 7.787 * var_Y ) + ( 16. / 116. )
    if (var_Z > 0.008856) :var_Z = var_Z ** ( 1. / 3. )
    else                  :var_Z = ( 7.787 * var_Z ) + ( 16. / 116. )

    CIE_L = (116. * var_Y) - 16.
    CIE_a = 500. * (var_X - var_Y)
    CIE_b = 200. * (var_Y - var_Z)

    LAB = np.zeros(3, np.float)
    LAB[0] = round(CIE_L)
    LAB[1] = round(CIE_a)
    LAB[2] = round(CIE_b)
    return LAB

def rgbToYxy(RGB):
    sR = RGB[2]
    sG = RGB[1]
    sB = RGB[0]

    var_R = (sR / 255.)
    var_G = (sG / 255.)
    var_B = (sB / 255.)

    if (var_R > 0.04045) :var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else                 :var_R = var_R / 12.92
    if (var_G > 0.04045) :var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else                 :var_G = var_G / 12.92
    if (var_B > 0.04045) :var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else                 :var_B = var_B / 12.92

    var_R = var_R * 100.
    var_G = var_G * 100.
    var_B = var_B * 100.

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)

    return (y,x)

def YxyTorgb(Yxy):

    Y = 100.
    y = Yxy[0]
    x = Yxy[1]
    if(y==0):
        return

    X = x * (Y / y)
    Z = (1 - x - y) * (Y / y)

    # XYZ -> RGB
    var_X = X / 100.
    var_Y = Y / 100.
    var_Z = Z / 100.

    var_R = var_X * 3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y * 1.8758 + var_Z * 0.0415
    var_B = var_X * 0.0557 + var_Y * -0.2040 + var_Z * 1.0570

    if (var_R > 0.0031308):
        var_R = 1.055 * (var_R ** (1 / 2.4)) - 0.055
    else:
        var_R = 12.92 * var_R
    if (var_G > 0.0031308):
        var_G = 1.055 * (var_G ** (1 / 2.4)) - 0.055
    else:
        var_G = 12.92 * var_G
    if (var_B > 0.0031308):
        var_B = 1.055 * (var_B ** (1 / 2.4)) - 0.055
    else:
        var_B = 12.92 * var_B

    if (var_R < 0.): var_R = 0.
    if (var_R > 1.): var_R = 1.
    if (var_G < 0.): var_G = 0.
    if (var_G > 1.): var_G = 1.
    if (var_B < 0.): var_B = 0.
    if (var_B > 1.): var_B = 1.

    sR = var_R * 255
    sG = var_G * 255
    sB = var_B * 255

    cdRGB = np.zeros(3, np.uint8)
    cdRGB[2] = sR
    cdRGB[1] = sG
    cdRGB[0] = sB
    # print cdRGB
    return cdRGB


def rgbToycbcr(rgbData):
    cdYcbcr = np.zeros(3, np.float)
    var_R = rgbData[0]/255.
    var_G = rgbData[1]/255.
    var_B = rgbData[2]/255.
    cdYcbcr[0] = (0.257*var_R + 0.504*var_G + 0.098*var_B) * 255.
    cdYcbcr[1] = ((-0.148*var_R - 0.291*var_G + 0.439*var_B) + 0.5) * 255.
    cdYcbcr[2] = ((0.439*var_R - 0.368*var_G - 0.071*var_B) + 0.5 ) * 255.
    return cdYcbcr

def rgbTohsv(rgbData):
    cdHsv = np.zeros(3, np.float)
    var_R = rgbData[0] / 255.
    var_G = rgbData[1] / 255.
    var_B = rgbData[2] / 255.
    var_Min = min(var_R, min(var_G, var_B))
    var_Max = max(var_R, max(var_G, var_B))
    del_Max = var_Max - var_Min
    V = var_Max
    H=0.
    S=0.
    if (del_Max == 0):
        H = 0
        S = 0
    else:
        S = del_Max / var_Max
        del_R = (((var_Max - var_R) / 6.) + (del_Max / 2.)) / del_Max
        del_G = (((var_Max - var_G) / 6.) + (del_Max / 2.)) / del_Max
        del_B = (((var_Max - var_B) / 6.) + (del_Max / 2.)) / del_Max

        if (var_R == var_Max):
            H = del_B - del_G
        elif ( var_G == var_Max ):
            H = (1 / 3) + del_R - del_B
        elif (var_B == var_Max):
            H = (2 / 3) + del_G - del_R

        if (H < 0):
            H += 1
        if (H > 1):
            H -= 1

        cdHsv[0] = H
        cdHsv[1] = S
        cdHsv[2] = V
        return cdHsv

def DrowLABPos(IdealRGB,ReadRGB):
    global imgLabOrg,imgLabOut

    def GetLabBox(Lab, i, j, offset=0):
        global height, CCS_LAB_B_MIN, CCS_LAB_A_MIN
        y = height - (abs(CCS_LAB_B_MIN) + Lab[i][j][2] + offset) - 1
        x = abs(CCS_LAB_A_MIN) + Lab[i][j][1] + offset
        return (x, y)

    #ReadTmp = np.zeros((4, 6, 3), np.int)
    LABtmpIdeal = np.zeros((4, 6, 3), np.int)
    LABtmpRead  = np.zeros((4, 6, 3), np.int)
    imgLabOut = copy.deepcopy(imgLabOrg)
    for i in range(0, 4):
       for j in range(0, 6):
           LABtmpIdeal[i,j] = rgbTolab(IdealRGB[i][j])
           LABtmpRead[i, j] = rgbTolab(ReadRGB[i][j])
           cv2.rectangle(imgLabOut, GetLabBox(LABtmpIdeal,i,j,-2), GetLabBox(LABtmpIdeal,i,j,2), IdealRGB[i][j], 1)
           cv2.rectangle(imgLabOut, GetLabBox(LABtmpRead, i, j, -2), GetLabBox(LABtmpRead, i, j, 2), ReadRGB[i][j],-1)
           cv2.line(imgLabOut, GetLabBox(LABtmpIdeal,i,j), GetLabBox(LABtmpRead, i, j,), (128, 128, 128), 1,lineType=8)
    return

def DrowYxyPos(IdealRGB,ReadRGB):
    global imgYxyOrg,imgYxyOut

    def GetYxyBox(Yxy,i, j, offset=0):
        y = 100-(int(Yxy[i][j][0]*100)+offset)
        x = int(Yxy[i][j][1]*100)+offset
        return (x, y)

    YxytmpIdeal = np.zeros((4, 6, 2), np.float)
    YxytmpRead  = np.zeros((4, 6, 2), np.float)
    imgYxyOut = copy.deepcopy(imgYxyOrg)
    for i in range(0, 4):
       for j in range(0, 6):
           YxytmpIdeal[i, j] = rgbToYxy(IdealRGB[i][j])
           YxytmpRead [i, j] = rgbToYxy(ReadRGB[i][j])

           cv2.rectangle(imgYxyOut, GetYxyBox(YxytmpIdeal, i, j, -2), GetYxyBox(YxytmpIdeal, i, j, 1), IdealRGB[i][j],
                         1)
           cv2.rectangle(imgYxyOut, GetYxyBox(YxytmpRead, i, j, -2), GetYxyBox(YxytmpRead, i, j, 1), ReadRGB[i][j],
                         -1)


    return

def ShowLabRect():
    global imgLabOut,imgYxyOut
    cv2.imshow('Lab', imgLabOut)
    cv2.imshow('Yxy', imgYxyOut)
    return




CCS_LAB_A_MIN=-70
CCS_LAB_A_MAX=80
CCS_LAB_B_MIN=-70
CCS_LAB_B_MAX=100

width =CCS_LAB_A_MAX-CCS_LAB_A_MIN
height =CCS_LAB_B_MAX-CCS_LAB_B_MIN


imgLabOrg = np.zeros((height,width,3), np.uint8)
imgLabOut = np.zeros((height, width, 3), np.uint8)

cdLAB = np.zeros(3, np.float)
cdLAB[0] = 90.
for b in range(CCS_LAB_B_MIN, CCS_LAB_B_MAX):
    for a in range(CCS_LAB_A_MIN, CCS_LAB_A_MAX):

        if a==0 or b==0:
            y = height - (abs(CCS_LAB_B_MIN) + b) - 1
            x = abs(CCS_LAB_A_MIN) + a
        else:
            cdLAB[1] = a
            cdLAB[2] = b
            y = height - (abs(CCS_LAB_B_MIN) + b) - 1
            x = abs(CCS_LAB_A_MIN)+a
            imgLabOrg[y,x] = labTorgb(cdLAB)
imgLabOut = copy.deepcopy(imgLabOrg)




imgYxyOrg = np.zeros((100, 100, 3), np.uint8)
imgYxyOut = np.zeros((100, 100, 3), np.uint8)
i=0
j=0
for b in np.linspace(0, 1,100):
    for a in np.linspace(1, 0,100):
        RGB = YxyTorgb((a, b))
        if(RGB is not None):
            if (RGB[0] != 0)and(RGB[1] !=0)and(RGB[2] !=0):
                imgYxyOrg[i,j]= RGB
        i+=1
    i = 0
    j += 1
imgYxyOut = copy.deepcopy(imgYxyOrg)


def CalcCcMatrix(Source,Target):
    Mat33 = np.dot(Source.T,Source)
    Mat33T = np.linalg.inv(Mat33)
    Mat3_24 = np.dot(Mat33T,Source.T)
    CCMT = np.dot(Mat3_24 , Target)
    for i in range(0, 3):
        rowSum = (CCMT[0][i] + CCMT[1][i] + CCMT[2][i])
        CCMT[0][i] /= rowSum
        CCMT[1][i] /= rowSum
        CCMT[2][i] /= rowSum
    CCMT = CCMT.T
    return CCMT

cv2.namedWindow('Lab',cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('Yxy',cv2.WINDOW_AUTOSIZE)
"""
#cv2.namedWindow('Lab', flags =cv2.WINDOW_NORMAL  )
cv2.namedWindow('Lab',cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('Yxy',cv2.WINDOW_AUTOSIZE)
while True:
    ShowLabRect()
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
        
cv2.destroyAllWindows()
"""