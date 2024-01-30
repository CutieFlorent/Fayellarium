# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 22:23:49 2023

@author: frank
"""

# -*- coding:utf-8 -*-
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
img = np.zeros((1500, 1700, 3), dtype=np.uint8)
img.fill(255)
N = 64
C = N*np.sin(np.pi/3)
skin = [(223,234,244),(191,223,234),(71,85,99)]


 
def AddText(img, text, pos, textColor=(0, 0, 0), textSize=64):
    x,y = pos
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))# 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)# 字体的格式
    fontStyle = ImageFont.truetype(
        "msyh.ttc", textSize, encoding="utf-8")# 绘制文本
    draw.text((x-textSize*0.5,y-textSize*0.75,),  #居中
              text, textColor, font=fontStyle)# 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def hex(center,radius,color):
    x,y = center
    doty = radius
    dots = []
    for i in range(6):
        x_ = doty*np.sin(np.pi/3*i)#+dots[0][0]*np.cos(np.pi/3*i)
        y_ = doty*np.cos(np.pi/3*i)#-dots[0][0]*np.sin(np.pi/3*i)
        dots.append([x+x_,y+y_])
    pts = np.array(dots,np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], color=color)
    
def coord(i,j,no = 1):
    if no == 1:t = 14-abs(i)
    elif no == 2:t = i
    else: t = 14-i
    cx = ox + 2*j*C - t*C
    cy = oy + 3/2*i*N
    return cx,cy
        
#hex([400,300],N,(0,0,0))
p1 = np.array([ ['','','','炮','炮','',],
                   ['','石','马','雷','马','石',],
                   ['石','雷','左','右','雷','石',],
                     ['象','右','都','左','象','',],
                          ['','左','右','','','',],])
p2 = np.rot90(p1,-1)
p3 = np.array([ ['','炮','炮','','','',],
                   ['石','马','雷','马','石','',],
                   ['石','雷','左','右','雷','石',],
                     ['','象','右','都','左','象',],
                          ['','','','左','右','',],])
p3 = np.rot90(p3,1)
#pieces = np.zeros((14,14),dtype='<U1')

ox,oy = 900,400
for i in range(-3,11):
    t = 14-abs(i)
    for j in range(t):
        cx,cy = coord(i,j,)
        hex((cx,cy),N,skin[2-(t+j) % 3])
        
for i in range(5):
    for j in range(6):
        cx,cy = coord(i+6,j,)
        text = p1[i,j]
        if text == '雷' or text == '都':
            img = AddText(img,text,(cx,cy),(255,0,0))
        else:img = AddText(img,text,(cx,cy))
        
for i in range(6):
    for j in range(5):
        cx,cy = coord(i-3,j-7,2)
        text = p2[i,j]
        if text == '雷' or text == '都':
            img = AddText(img,text,(cx,cy),(255,0,0))
        else:img = AddText(img,text,(cx,cy))
        
for i in range(6):
    for j in range(5):
        cx,cy = coord(i-3,j+9,3)
        text = p3[i,j]
        if text == '雷' or text == '都':
            img = AddText(img,text,(cx,cy),(255,0,0))
        else:img = AddText(img,text,(cx,cy))

    
#cv2.imshow('img', img)
cv2.imwrite('chessB.png',img)
cv2.waitKey()


#pts = np.array([[10, 10], [400, 10],[450, 30], [400, 400], [10, 400]], np.int32)  # 数据类型必须为 int32
#pts = pts.reshape((-1, 1, 2))
 
# 绘制未填充的多边形
#cv2.polylines(img, [pts], isClosed=True, color=(0,0,255), thickness=1)
 
# 绘制填充的多边形
#cv2.fillPoly(img, [pts], color=(255, 255, 0))
#石：不能被除了炸以外的棋子吃掉，起到挡路作用，一次移动一格
#炸：用来炸石，炸完之后同归于尽，一次移动一格
#马：一次移动2格之后再斜60度移一格，无视中间障碍
#象：一次可选定周围六个同色格子的一个，移动至该格子，或者保持方向移动至更远的同色格子。
#左：一次可移动3格（待议），但只能吃自己左手侧玩家的棋子。
#右：一次可移动3格（待议），但只能吃自己右手侧玩家的棋子。
            #cv2.imwrite('sb\\{}{}.png'.format(i,j),img)
    #if i==10:cv2.imwrite('{}.png'.format(i),img)
