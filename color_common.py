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
RectInsindBoxPos = np.zeros((4,6,2), np.int)
ROB_Size = 4
RIB_Size = 10

DragBoxPosX=-1
DragBoxPosY=-1

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
    for i in range(0, 3):
        for j in range(0, 3):
            if (x >= RectOutBoxPos[i][j][0] - ROB_Size) and (x <= RectOutBoxPos[i][j][0] + ROB_Size) and (
                        y >= RectOutBoxPos[i][j][1] - ROB_Size) and (y <= RectOutBoxPos[i][j][1] + ROB_Size):
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

    img = np.zeros(img_Org.shape, np.int)
    img = copy.deepcopy(img_Org)

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

    draw_RectIn()

    imgOut = copy.deepcopy(img)


def Cal_RectIn():
    global img, img_Org, imgOut, RectOutBoxPos, RectInsindBoxPos

    ww = (abs(RectOutBoxPos[2][2][0] - RectOutBoxPos[0][0][0]))
    hh = (abs(RectOutBoxPos[2][2][1] - RectOutBoxPos[0][0][1]))
    InBoxSizeW = ww / 6
    InBoxSizeH = hh / 4

    for j in range(0, 6):
        RectInsindBoxPos[0][j][0] = RectOutBoxPos[0][0][0] + (j * InBoxSizeW) + InBoxSizeW / 2
        RectInsindBoxPos[1][j][0] = RectOutBoxPos[0][0][0] + (j * InBoxSizeW) + InBoxSizeW / 2
        RectInsindBoxPos[2][j][0] = RectOutBoxPos[0][0][0] + (j * InBoxSizeW) + InBoxSizeW / 2
        RectInsindBoxPos[3][j][0] = RectOutBoxPos[0][0][0] + (j * InBoxSizeW) + InBoxSizeW / 2

    for j in range(0, 4):
        RectInsindBoxPos[j][0][1] = RectOutBoxPos[0][0][1] + (j * InBoxSizeH) + InBoxSizeH / 2
        RectInsindBoxPos[j][1][1] = RectOutBoxPos[0][0][1] + (j * InBoxSizeH) + InBoxSizeH / 2
        RectInsindBoxPos[j][2][1] = RectOutBoxPos[0][0][1] + (j * InBoxSizeH) + InBoxSizeH / 2
        RectInsindBoxPos[j][3][1] = RectOutBoxPos[0][0][1] + (j * InBoxSizeH) + InBoxSizeH / 2
        RectInsindBoxPos[j][4][1] = RectOutBoxPos[0][0][1] + (j * InBoxSizeH) + InBoxSizeH / 2
        RectInsindBoxPos[j][5][1] = RectOutBoxPos[0][0][1] + (j * InBoxSizeH) + InBoxSizeH / 2
    return 0



def draw_RectIn():
    global img, img_Org, imgOut, RectInsindBoxPos,RIB_Size
    Cal_RectIn()


    for i in range(0, 4):
        for j in range(0, 6):
            cv2.rectangle(img, GetInBoxPos(i, j, -RIB_Size), GetInBoxPos(i, j, RIB_Size), (255, 0, 0), 1)

    SumRgb_RectIn()
    draw_RectInerIn()

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
    global img, img_Org, imgOut, RectInsindBoxPos, RIB_Size,cdIdealRGB
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



def draw_circle(event, x,y, flags, param):
    global drawing, img, img_Org, imgOut,RectOutBoxPos,DragBoxPosX,DragBoxPosY


    if event == cv2.EVENT_LBUTTONDOWN:
        DragBoxPosY,DragBoxPosX = Check_RectOutBoxIn(x, y)

        if DragBoxPosX==-1 or DragBoxPosY==-1 :
            drawing = 1
            RectOutBoxPos[0][0][0] = x
            RectOutBoxPos[0][0][1] = y
            print "new box",drawing
        elif DragBoxPosX == 1 and DragBoxPosY == 1:
            drawing = 3
            print "move box"
        else:
            drawing = 2
            print "modi box", DragBoxPosY,DragBoxPosX


    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == 1:
           img = np.zeros(img_Org.shape, np.int)
           img = copy.deepcopy(img_Org)
           cv2.rectangle(img,GetOutBoxPos(0,0),(x,y),(255,0,0),1)
           imgOut = copy.deepcopy(img)

        elif drawing == 3:
            moveX=RectOutBoxPos[1][1][0]-x
            moveY=RectOutBoxPos[1][1][1]-y
            for i in range(0, 3):
                for j in range(0, 3):
                    RectOutBoxPos[i][j][0] = RectOutBoxPos[i][j][0] - moveX
                    RectOutBoxPos[i][j][1] = RectOutBoxPos[i][j][1] - moveY
            draw_RectOut()

        elif drawing == 2:
            RectOutBoxPos[DragBoxPosY][DragBoxPosX][0] = x
            RectOutBoxPos[DragBoxPosY][DragBoxPosX][1] = y
            draw_RectOut()



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
            draw_RectOut()

        elif drawing == 3:
            drawing = 9
        elif  drawing == 2:
            drawing = 9
            RectOutBoxPos[DragBoxPosY][DragBoxPosX][0] = x
            RectOutBoxPos[DragBoxPosY][DragBoxPosX][1] = y
            draw_RectOut()




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
