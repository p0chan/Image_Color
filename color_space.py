import cv2
import pandas as pd
import numpy as np

CCS_LAB_A_MIN=-70
CCS_LAB_A_MAX=90
CCS_LAB_B_MIN=-60
CCS_LAB_B_MAX=100

CCS_LAB_X_RANGE=160
CCS_LAB_Y_RANGE=160




def labTorgb(labData):

    #LAB -> XYZ
    XYZData = np.zeros(3, np.float)
    XYZData[1] = ( labData[0] + 16. ) / 116.
    XYZData[0] = labData[1] / 500. + XYZData[1]
    XYZData[2] = XYZData[1] - labData[2] / 200.

    if ( pow(XYZData[1], 3.0) > 0.008856 ) :
        XYZData[1] = pow(XYZData[1], 3.0)
    else:
        XYZData[1] = ( XYZData[1] - 16. / 116.0 ) / 7.787

    if ( pow(XYZData[0], 3.0) > 0.008856 ) :
        XYZData[0] = pow(XYZData[0], 3.0)
    else:
        XYZData[0] = ( XYZData[0] - 16. / 116.0 ) / 7.787
    
    if ( pow(XYZData[2], 3.0) > 0.008856 ) :
        XYZData[2] = pow(XYZData[2], 3.0)
    else:
        XYZData[2] = ( XYZData[2] - 16. / 116.0 ) / 7.787
    
    X = 95.047 * XYZData[0]
    Y = 100. * XYZData[1]
    Z = 108.883 * XYZData[2]
    #print X,Y,Z

    # XYZ -> RGB
    RGBDATA = np.zeros(3, np.float)
    XYZData[0] = X / 100.
    XYZData[1] = Y / 100.
    XYZData[2] = Z / 100.

    RGBDATA[0] = XYZData[0] *  3.2406 + XYZData[1] * -1.5372 + XYZData[2] * -0.4986
    RGBDATA[1] = XYZData[0] * -0.9689 + XYZData[1] *  1.8758 + XYZData[2] *  0.0415
    RGBDATA[2] = XYZData[0] *  0.0557 + XYZData[1] * -0.2040 + XYZData[2] *  1.0570

    if ( RGBDATA[0] > 0.0031308 ) :
        RGBDATA[0] = 1.055 * pow( RGBDATA[0], ( 1 / 2.4 ) ) - 0.055
    else:
        RGBDATA[0] = 12.92 * RGBDATA[0]

    if ( RGBDATA[1] > 0.0031308 ) :
        RGBDATA[1] = 1.055 * pow( RGBDATA[1], ( 1 / 2.4 ) ) - 0.055
    else:
        RGBDATA[1] = 12.92 * RGBDATA[1]

    if ( RGBDATA[2] > 0.0031308 ) :
        RGBDATA[2] = 1.055 * pow( RGBDATA[2], ( 1 / 2.4 ) ) - 0.055
    else:
        RGBDATA[2] = 12.92 * RGBDATA[2]

    if (RGBDATA[0] < 0):
        RGBDATA[0] = 0
    if (RGBDATA[0] > 1):
        RGBDATA[0] = 1

    if (RGBDATA[1] < 0):
        RGBDATA[1] = 0
    if (RGBDATA[1] > 1):
        RGBDATA[1] = 1

    if (RGBDATA[1] < 0):
        RGBDATA[1] = 0
    if (RGBDATA[1] > 1):
        RGBDATA[1] = 1

    cdRGB = np.zeros(3, np.int)
    cdRGB[2] = RGBDATA[0] * 255
    cdRGB[1] = RGBDATA[1] * 255
    cdRGB[0] = RGBDATA[2] * 255

    return cdRGB



cv2.namedWindow('imgLab', flags =cv2.WINDOW_NORMAL  )
imgLab = np.zeros(((CCS_LAB_B_MAX-CCS_LAB_B_MIN),(CCS_LAB_A_MAX-CCS_LAB_A_MIN),3), np.uint8)

cdLAB = np.zeros(3, np.float)
cdLAB[0] = 90
for b in range(CCS_LAB_B_MIN, CCS_LAB_B_MAX):
    for a in range(CCS_LAB_A_MIN, CCS_LAB_A_MAX):
        cdLAB[1] = a
        cdLAB[2] = b
        imgLab[abs(CCS_LAB_B_MIN) + b, abs(CCS_LAB_A_MIN) + a] = labTorgb(cdLAB)






while True:
    cv2.imshow('imgLab', imgLab)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()