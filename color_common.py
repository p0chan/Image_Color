import cv2
import pandas as pd
import numpy as np
import copy

import INI_Config as ini
import color_space as cp



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
img = copy.deepcopy(img_Org)

imgOut = np.zeros(img_Org.shape, np.int)
imgOut = copy.deepcopy(img_Org)


drawing = 0
RectOutBoxPos = np.zeros((3,3,2), np.int)
RectInsindBoxPos = np.zeros((4,6,2), np.int)
ROB_Size = 4
RIB_Size = 10

DragOutBoxPosY=-1
DragOutBoxPosX=-1

DragInBoxPosY=-1
DragInBoxPosX=-1

ini.OpenFile('config')
#print ini.GetSectionS()
#print ini.GetItemS('OutBox')
#print ini.GetOptionS('OutBox')



#http://xritephoto.com/documents/literature/en/ColorData-1p_EN.pdf
cdIdealRGB = np.zeros((4,6,3), np.int)
cdIdealRGB = \
    [[[68,82,115],     [130,150,194],     [157,122,98],     [67,108,87],     [177,128,133],     [170,189,103]],
     [[44,126,224],     [166,91,80],     [99,90,193],     [108,60,94],     [64,188,157],     [46,163,224]],
     [[150,61,56],     [73,148,70],     [60,54,175],     [31,199,231],     [149,86,187],     [161,133,8]],
     [[243,243,242],     [200,200,200],     [160,160,160],     [122,122,121],     [85,85,85],     [52,52,52]]]

ReadRGB = np.zeros((4,6,3), np.int)




def GetOutBoxPos(y,x,Offset=0):
    global RectOutBoxPos
    return RectOutBoxPos[y][x][0]+Offset,RectOutBoxPos[y][x][1]+Offset

def GetInBoxPos(y,x,Offset=0):
    global RectOutBoxPos
    return RectInsindBoxPos[y][x][0]+Offset,RectInsindBoxPos[y][x][1]+Offset



def Check_RectOutBoxIn(x,y):
    global RectOutBoxPos,ROB_Size

    DragSize = ROB_Size+2
    for i in range(0, 3):
        for j in range(0, 3):
            if (x >= RectOutBoxPos[i][j][0] - DragSize) and (x <= RectOutBoxPos[i][j][0] + DragSize) and (
                        y >= RectOutBoxPos[i][j][1] - DragSize) and (y <= RectOutBoxPos[i][j][1] + DragSize):
                return i, j
    return -1,-1

def Check_RectInBoxIn(x,y):
    global RectOutBoxPos,RIB_Size

    DragSize = RIB_Size+2
    for i in range(0, 4):
        for j in range(0, 6):
            if (x >= RectInsindBoxPos[i][j][0] - DragSize) and (x <= RectInsindBoxPos[i][j][0] + DragSize) and (
                        y >= RectInsindBoxPos[i][j][1] - DragSize) and (y <= RectInsindBoxPos[i][j][1] + DragSize):
                return i, j
    return -1,-1

def Cal_RectOut():
    global img, img_Org, imgOut, RectOutBoxPos, ROB_Size

    if (RectOutBoxPos[0][0][0] > RectOutBoxPos[2][2][0]):
        tmp = RectOutBoxPos[2][2][0]
        RectOutBoxPos[2][2][0] = RectOutBoxPos[0][0][0]
        RectOutBoxPos[0][0][0] = tmp
    if (RectOutBoxPos[0][0][1] > RectOutBoxPos[2][2][1]):
        tmp = RectOutBoxPos[2][2][1]
        RectOutBoxPos[2][2][1] = RectOutBoxPos[0][0][1]
        RectOutBoxPos[0][0][1] = tmp

    RectOutBoxPos[0][1][0] = RectOutBoxPos[0][0][0] + ((RectOutBoxPos[2][2][0]-RectOutBoxPos[0][0][0])/2)
    RectOutBoxPos[0][1][1] = RectOutBoxPos[0][0][1]

    RectOutBoxPos[0][2][0] = RectOutBoxPos[2][2][0]
    RectOutBoxPos[0][2][1] = RectOutBoxPos[0][0][1]

    RectOutBoxPos[1][0][0] = RectOutBoxPos[0][0][0]
    RectOutBoxPos[1][0][1] = RectOutBoxPos[0][0][1] + ((RectOutBoxPos[2][2][1]-RectOutBoxPos[0][0][1])/2)

    RectOutBoxPos[1][1][0] = RectOutBoxPos[0][0][0] + ((RectOutBoxPos[2][2][0]-RectOutBoxPos[0][0][0])/2)
    RectOutBoxPos[1][1][1] = RectOutBoxPos[0][0][1] + ((RectOutBoxPos[2][2][1]-RectOutBoxPos[0][0][1])/2)

    RectOutBoxPos[1][2][0] = RectOutBoxPos[2][2][0]
    RectOutBoxPos[1][2][1] = RectOutBoxPos[0][0][1] + ((RectOutBoxPos[2][2][1]-RectOutBoxPos[0][0][1])/2)

    RectOutBoxPos[2][0][0] = RectOutBoxPos[0][0][0]
    RectOutBoxPos[2][0][1] = RectOutBoxPos[2][2][1]

    RectOutBoxPos[2][1][0] = RectOutBoxPos[0][0][0] + ((RectOutBoxPos[2][2][0]-RectOutBoxPos[0][0][0])/2)
    RectOutBoxPos[2][1][1] = RectOutBoxPos[2][2][1]

def draw_RectOut():
    global img,img_Org,imgOut,RectOutBoxPos,ROB_Size

    cv2.line(img, GetOutBoxPos(0,0), GetOutBoxPos(0,1), (255, 255, 255), 1)
    cv2.line(img, GetOutBoxPos(0,1), GetOutBoxPos(0,2), (255, 255, 255), 1)

    cv2.line(img, GetOutBoxPos(2, 0), GetOutBoxPos(2, 1), (255, 255, 255), 1)
    cv2.line(img, GetOutBoxPos(2, 1), GetOutBoxPos(2, 2), (255, 255, 255), 1)

    cv2.line(img, GetOutBoxPos(0, 0), GetOutBoxPos(1, 0), (255, 255, 255), 1)
    cv2.line(img, GetOutBoxPos(1, 0), GetOutBoxPos(2, 0), (255, 255, 255), 1)

    cv2.line(img, GetOutBoxPos(0, 2), GetOutBoxPos(1, 2), (255, 255, 255), 1)
    cv2.line(img, GetOutBoxPos(1, 2), GetOutBoxPos(2, 2), (255, 255, 255), 1)

    for i in range(0, 3):
        for j in range(0, 3):
            cv2.rectangle(img, GetOutBoxPos(i, j, -ROB_Size), GetOutBoxPos(i, j, ROB_Size), (255, 255, 255), 1)

    ini.SetData('OutBox', 'Postion', RectOutBoxPos.tolist())
    ini.SetData('OutBox', 'ROB_Size', ROB_Size)
    ini.FlashFile()





def Cal_RectIn():
    global img, img_Org, imgOut, RectOutBoxPos, RectInsindBoxPos

    InBoxSizeW14 = np.zeros(2, np.int)
    InBoxSizeW24 = np.zeros(2, np.int)
    InBoxSizeW34 = np.zeros(2, np.int)
    InBoxSizeW44 = np.zeros(2, np.int)
    InBoxSizeH14 = np.zeros(3, np.int)
    InBoxSizeH24 = np.zeros(3, np.int)
    InBoxSizeH34 = np.zeros(3, np.int)
    InBoxSizeH44 = np.zeros(3, np.int)

    leftX = np.zeros(4, np.int)
    midX = np.zeros(4, np.int)
    rightX = np.zeros(4, np.int)
    upY  = np.zeros(6, np.int)
    midY = np.zeros(6, np.int)
    downY = np.zeros(6, np.int)


    lP1 = GetOutBoxPos(0, 0)
    lP2 = GetOutBoxPos(1, 0)
    lP3 = GetOutBoxPos(2, 0)
    leftX[0] = lP1[0] + ((lP2[0] - lP1[0]) / 4)
    leftX[1] = lP1[0] + ((lP2[0] - lP1[0]) / 4) * 3
    leftX[2] = lP2[0] + ((lP3[0] - lP2[0]) / 4)
    leftX[3] = lP2[0] + ((lP3[0] - lP2[0]) / 4) * 3

    wmP1 = GetOutBoxPos(0, 1)
    wmP2 = GetOutBoxPos(1, 1)
    wmP3 = GetOutBoxPos(2, 1)
    midX[0] = wmP1[0] + ((wmP2[0] - wmP1[0]) / 4)
    midX[1] = wmP1[0] + ((wmP2[0] - wmP1[0]) / 4) * 3
    midX[2] = wmP2[0] + ((wmP3[0] - wmP2[0]) / 4)
    midX[3] = wmP2[0] + ((wmP3[0] - wmP2[0]) / 4) * 3

    rP1 = GetOutBoxPos(0, 2)
    rP2 = GetOutBoxPos(1, 2)
    rP3 = GetOutBoxPos(2, 2)
    rightX[0] = rP1[0] + ((rP2[0] - rP1[0]) / 4)
    rightX[1] = rP1[0] + ((rP2[0] - rP1[0]) / 4) * 3
    rightX[2] = rP2[0] + ((rP3[0] - rP2[0]) / 4)
    rightX[3] = rP2[0] + ((rP3[0] - rP2[0]) / 4) * 3


    InBoxSizeW14[0] = (abs(leftX[0] - midX[0])) / 3
    InBoxSizeW14[1] = (abs(leftX[1] - midX[1])) / 3

    InBoxSizeW24[0] = (abs(rightX[0] - midX[0])) / 3
    InBoxSizeW24[1] = (abs(rightX[1] - midX[1])) / 3

    InBoxSizeW34[0] = (abs(leftX[2] - midX[2])) / 3
    InBoxSizeW34[1] = (abs(leftX[3] - midX[3])) / 3

    InBoxSizeW44[0] = (abs(rightX[2] - midX[2])) / 3
    InBoxSizeW44[1] = (abs(rightX[3] - midX[3])) / 3


    for j in range(0, 3):
        RectInsindBoxPos[0][j][0] = leftX[0] + (j * InBoxSizeW14[0]) + InBoxSizeW14[0] / 2
        RectInsindBoxPos[1][j][0] = leftX[1] + (j * InBoxSizeW14[1]) + InBoxSizeW14[1] / 2
        RectInsindBoxPos[2][j][0] = leftX[2] + (j * InBoxSizeW34[0]) + InBoxSizeW34[0] / 2
        RectInsindBoxPos[3][j][0] = leftX[3] + (j * InBoxSizeW34[1]) + InBoxSizeW34[1] / 2
        RectInsindBoxPos[0][3+j][0] = midX[0] + (3+j * InBoxSizeW24[0]) + InBoxSizeW24[0] / 2
        RectInsindBoxPos[1][3+j][0] = midX[1] + (3+j * InBoxSizeW24[1]) + InBoxSizeW24[1] / 2
        RectInsindBoxPos[2][3+j][0] = midX[2] + (3+j * InBoxSizeW44[0]) + InBoxSizeW44[0] / 2
        RectInsindBoxPos[3][3+j][0] = midX[3] + (3+j * InBoxSizeW44[1]) + InBoxSizeW44[1] / 2

    uP1 = GetOutBoxPos(0, 0)
    uP2 = GetOutBoxPos(0, 1)
    uP3 = GetOutBoxPos(0, 2)
    upY[0] = uP1[1] + ((uP2[1] - uP1[1]) / 6)
    upY[1] = uP1[1] + ((uP2[1] - uP1[1]) / 6) * 3
    upY[2] = uP1[1] + ((uP2[1] - uP1[1]) / 6) * 5

    upY[3] = uP2[1] + ((uP3[1] - uP2[1]) / 6)
    upY[4] = uP2[1] + ((uP3[1] - uP2[1]) / 6) * 3
    upY[5] = uP2[1] + ((uP3[1] - uP2[1]) / 6) * 5

    mhP1 = GetOutBoxPos(1, 0)
    mhP2 = GetOutBoxPos(1, 1)
    mhP3 = GetOutBoxPos(1, 2)
    midY[0] = mhP1[1] + ((mhP2[1] - mhP1[1]) / 6)
    midY[1] = mhP1[1] + ((mhP2[1] - mhP1[1]) / 6) * 3
    midY[2] = mhP1[1] + ((mhP2[1] - mhP1[1]) / 6) * 5

    midY[3] = mhP2[1] + ((mhP3[1] - mhP2[1]) / 6)
    midY[4] = mhP2[1] + ((mhP3[1] - mhP2[1]) / 6) * 3
    midY[5] = mhP2[1] + ((mhP3[1] - mhP2[1]) / 6) * 5


    dP1 = GetOutBoxPos(2, 0)
    dP2 = GetOutBoxPos(2, 1)
    dP3 = GetOutBoxPos(2, 2)
    downY[0] = dP1[1] + ((dP2[1] - dP1[1]) / 6)
    downY[1] = dP1[1] + ((dP2[1] - dP1[1]) / 6) * 3
    downY[2] = dP1[1] + ((dP2[1] - dP1[1]) / 6) * 5

    downY[3] = dP2[1] + ((dP3[1] - dP2[1]) / 6)
    downY[4] = dP2[1] + ((dP3[1] - dP2[1]) / 6) * 3
    downY[5] = dP2[1] + ((dP3[1] - dP2[1]) / 6) * 5

    InBoxSizeH14[0] = (abs(midY[0] - upY[0])) / 2
    InBoxSizeH14[1] = (abs(midY[1] - upY[1])) / 2
    InBoxSizeH14[2] = (abs(midY[2] - upY[2])) / 2

    InBoxSizeH24[0] = (abs(midY[3] - upY[3])) / 2
    InBoxSizeH24[1] = (abs(midY[4] - upY[4])) / 2
    InBoxSizeH24[2] = (abs(midY[5] - upY[5])) / 2

    InBoxSizeH34[0] = (abs(downY[0] - midY[0])) / 2
    InBoxSizeH34[1] = (abs(downY[1] - midY[1])) / 2
    InBoxSizeH34[2] = (abs(downY[2] - midY[2])) / 2

    InBoxSizeH44[0] = (abs(downY[3] - midY[3])) / 2
    InBoxSizeH44[1] = (abs(downY[4] - midY[4])) / 2
    InBoxSizeH44[2] = (abs(downY[5] - midY[5])) / 2


    for j in range(0, 2):
        RectInsindBoxPos[j][0][1] = upY[0] + (j * InBoxSizeH14[0]) + InBoxSizeH14[0] / 2
        RectInsindBoxPos[j][1][1] = upY[1] + (j * InBoxSizeH14[1]) + InBoxSizeH14[1] / 2
        RectInsindBoxPos[j][2][1] = upY[2] + (j * InBoxSizeH14[2]) + InBoxSizeH14[2] / 2

        RectInsindBoxPos[j][3][1] = upY[3] + (j * InBoxSizeH24[0]) + InBoxSizeH24[0] / 2
        RectInsindBoxPos[j][4][1] = upY[4] + (j * InBoxSizeH24[1]) + InBoxSizeH24[1] / 2
        RectInsindBoxPos[j][5][1] = upY[5] + (j * InBoxSizeH24[2]) + InBoxSizeH24[2] / 2

        RectInsindBoxPos[2+j][0][1] = midY[0] + (j * InBoxSizeH34[0]) + InBoxSizeH34[0] / 2
        RectInsindBoxPos[2+j][1][1] = midY[1] + (j * InBoxSizeH34[1]) + InBoxSizeH34[1] / 2
        RectInsindBoxPos[2+j][2][1] = midY[2] + (j * InBoxSizeH34[2]) + InBoxSizeH34[2] / 2

        RectInsindBoxPos[2+j][3][1] = midY[3] + (j * InBoxSizeH44[0]) + InBoxSizeH44[0] / 2
        RectInsindBoxPos[2+j][4][1] = midY[4] + (j * InBoxSizeH44[1]) + InBoxSizeH44[1] / 2
        RectInsindBoxPos[2+j][5][1] = midY[5] + (j * InBoxSizeH44[2]) + InBoxSizeH44[2] / 2



    return 0



def draw_RectIn():
    global img, img_Org, imgOut, RectInsindBoxPos,RIB_Size

    for i in range(0, 4):
        for j in range(0, 6):
            cv2.rectangle(img, GetInBoxPos(i, j, -RIB_Size), GetInBoxPos(i, j, RIB_Size), (255, 0, 0), 1)

    SumRgb_RectIn()
    draw_RectInerIn()
    ini.SetData('InBox', 'Postion', RectInsindBoxPos.tolist())
    ini.SetData('InBox', 'RIB_Size', RIB_Size)
    ini.FlashFile()

    cp.DrowLABPos(cdIdealRGB, ReadRGB)
    cp.DrowYxyPos(cdIdealRGB, ReadRGB)
    cp.ShowLabRect()

    TEXT_OUT()
    return

def SumRgb_RectIn():
    global img, img_Org, imgOut, RectInsindBoxPos, RIB_Size

    for i in range(0, 4):
        for j in range(0, 6):
            ReadRGB[i][j][0] = 0
            ReadRGB[i][j][1] = 0
            ReadRGB[i][j][2] = 0

    for i in range(0, 4):
        for j in range(0, 6):
            xx, yy = GetInBoxPos(i, j, -RIB_Size)
            for z in range(0, RIB_Size):
                for l in range(0, RIB_Size):
                    ReadRGB[i][j][0] += img_Org[yy+z][xx+l][0]
                    ReadRGB[i][j][1] += img_Org[yy+z][xx+l][1]
                    ReadRGB[i][j][2] += img_Org[yy+z][xx+l][2]
            ReadRGB[i][j][0] = ReadRGB[i][j][0]/(RIB_Size*RIB_Size)
            ReadRGB[i][j][1] = ReadRGB[i][j][1]/(RIB_Size*RIB_Size)
            ReadRGB[i][j][2] = ReadRGB[i][j][2]/(RIB_Size*RIB_Size)


def draw_RectInerIn():
    global img, img_Org, imgOut, RectInsindBoxPos, RIB_Size,cdIdealRGB,ReadRGB
    InSizeX = RIB_Size/3
    InSizeY = RIB_Size/2

    for i in range(0, 4):
        for j in range(0, 6):
            xx1, yy1 = GetInBoxPos(i, j, -RIB_Size)
            xx2, yy2 = GetInBoxPos(i, j, RIB_Size)
            xx1 = xx2 - InSizeX
            yy2 = yy1 + InSizeY
            cv2.rectangle(img, (xx1, yy1),(xx2, yy2), ReadRGB[i][j], -1)

    for i in range(0, 4):
        for j in range(0, 6):
            xx1, yy1 = GetInBoxPos(i, j, -RIB_Size)
            xx2, yy2 = GetInBoxPos(i, j, RIB_Size)
            xx1 = xx2 - InSizeX
            yy1 = yy2 - InSizeY
            cv2.rectangle(img, (xx1, yy1),(xx2, yy2), cdIdealRGB[i][j], -1)
    return




def Cal_BOX():
    return 0

def draw_BOX():
    return 0

def draw_circle(event, x,y, flags, param):
    global drawing, img, img_Org, imgOut,RectOutBoxPos,DragOutBoxPosX,DragOutBoxPosY,DragInBoxPosX,DragInBoxPosY


    if event == cv2.EVENT_LBUTTONDOWN:

        DragOutBoxPosY,DragOutBoxPosX = Check_RectOutBoxIn(x, y)
        DragInBoxPosY, DragInBoxPosX = Check_RectInBoxIn(x, y)

        if DragInBoxPosY!=-1 and DragInBoxPosX!=-1 :
            # print "move In box"
            drawing = 4
        elif DragOutBoxPosY == 1 and DragOutBoxPosX == 1:
            drawing = 3
            # print "move outbox"
        elif DragOutBoxPosY != -1 and DragOutBoxPosX != -1:
            drawing = 2
            #print "move outbox"
        else:
            drawing = 1
            RectOutBoxPos[0][0][0] = x
            RectOutBoxPos[0][0][1] = y
            # print "new box",drawing


    elif event == cv2.EVENT_MOUSEMOVE:


        if drawing == 1:
           img = np.zeros(img_Org.shape, np.int)
           img = copy.deepcopy(img_Org)
           cv2.rectangle(img,GetOutBoxPos(0,0),(x,y),(255,0,0),1)
           imgOut = copy.deepcopy(img)

        elif drawing == 3:
            img = np.zeros(img_Org.shape, np.int)
            img = copy.deepcopy(img_Org)
            moveX=RectOutBoxPos[1][1][0]-x
            moveY=RectOutBoxPos[1][1][1]-y
            for i in range(0, 3):
                for j in range(0, 3):
                    RectOutBoxPos[i][j][0] = RectOutBoxPos[i][j][0] - moveX
                    RectOutBoxPos[i][j][1] = RectOutBoxPos[i][j][1] - moveY
            for i in range(0, 4):
                for j in range(0, 6):
                    RectInsindBoxPos[i][j][0] = RectInsindBoxPos[i][j][0] - moveX
                    RectInsindBoxPos[i][j][1] = RectInsindBoxPos[i][j][1] - moveY
            draw_RectOut()
            draw_RectIn()

        elif drawing == 2:
            img = np.zeros(img_Org.shape, np.int)
            img = copy.deepcopy(img_Org)
            RectOutBoxPos[DragOutBoxPosY][DragOutBoxPosX][0] = x
            RectOutBoxPos[DragOutBoxPosY][DragOutBoxPosX][1] = y
            draw_RectOut()
            Cal_RectIn()
            draw_RectIn()

        elif drawing == 4:
            img = np.zeros(img_Org.shape, np.int)
            img = copy.deepcopy(img_Org)
            RectInsindBoxPos[DragInBoxPosY][DragInBoxPosX][0] = x
            RectInsindBoxPos[DragInBoxPosY][DragInBoxPosX][1] = y
            draw_RectOut()
            draw_RectIn()


        imgOut = copy.deepcopy(img)


    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == 1:
            if abs(RectOutBoxPos[0][0][0] - x) < 20 or abs(RectOutBoxPos[0][0][1] - y) < 20 :
                drawing=0
                print "box to small"
                return
            RectOutBoxPos[2][2][0] = x
            RectOutBoxPos[2][2][1] = y
            drawing = 9
            Cal_RectOut()
            Cal_RectIn()
        elif drawing == 4:
            drawing = 9
        elif drawing == 3:
            drawing = 9
        elif  drawing == 2:
            drawing = 9
            RectOutBoxPos[DragOutBoxPosY][DragOutBoxPosX][0] = x
            RectOutBoxPos[DragOutBoxPosY][DragOutBoxPosX][1] = y

        draw_RectOut()
        draw_RectIn()
        imgOut = copy.deepcopy(img)

def TEXT_OUT():
    global imgOut
    dblSaturation=0
    dblMean=0
    dblMax=0
    dblColor1=0
    dblHSVSaturation=0
    TEXT1 = "saturation :%0.2f%% " % (dblSaturation)
    TEXT2 = 'diff mean :%0.2f'  % (dblMean)
    TEXT3 = 'diff max : %0.2f'  % (dblMax)
    TEXT4 = 'Y Level : %0.2f'  % (dblColor1)
    TEXT5 = 'HSV Saturation : %0.2f'  % (dblHSVSaturation/6)

    cv2.putText(imgOut, TEXT1, (1, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(imgOut, TEXT2, (1, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(imgOut, TEXT3, (1, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(imgOut, TEXT4, (1, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(imgOut, TEXT5, (1, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return 0

#cv2.namedWindow('imgOut', flags =cv2.WINDOW_NORMAL  )
cv2.namedWindow('imgOut',cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('imgOut',draw_circle)



if(ini.IsOption('OutBox','postion')) :
    RectOutBoxPos = np.asarray(ini.GetList('OutBox', 'postion'))
    draw_RectOut()

if(ini.IsOption('InBox','postion')) :
    RectInsindBoxPos = np.asarray(ini.GetList('InBox', 'postion'))
    draw_RectIn()

if (ini.IsOption('OutBox', 'rob_size')):
    ROB_Size = ini.GetDataInt('OutBox', 'rob_size')

if (ini.IsOption('InBox', 'rib_size')):
    RIB_Size = ini.GetDataInt('InBox', 'rib_size')


#img_Org = cv2.resize(img_Org, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
#img_Org = cv2.resize(img_Org, (jpgwidth*2, jpgheight*2), interpolation=cv2.INTER_CUBIC)


while True:

    cv2.imshow('imgOut', imgOut)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
