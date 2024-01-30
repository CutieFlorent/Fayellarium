# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 22:23:49 2023

@author: frank
"""

# -*- coding:utf-8 -*-
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
img = np.zeros((1800, 1500, 3), dtype=np.uint8)
img.fill(255)
N = 64
C = N*np.sin(np.pi/3)
skin = [(255,224,192),(255,255,255),(192,224,255)]
tone = ['C','D','E','F','G','A','B']

 
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
    cv2.polylines(img, [pts],isClosed=True, color=(0,0,0))
    
def coord(i,j):

    if i%2 == 0:
        cx = ox + 2*j*C + C/2
    else:
        cx = ox + 2*j*C - C/2
    cy = oy + 3/2*i*N
    return cx,cy
        
#hex([400,300],N,(0,0,0))

#pieces = np.zeros((14,14),dtype='<U1')

ox,oy = 200,400
for i in range(0,13):
    for j in range(10+i%2):
        cx,cy = coord(i,j)
        #calculate s
        s = 1
        if j-i%2/2 <3:
            s = 0
        elif j-i%2/2 >6:
            s = 2
        #text
        if j == 0:
            o = int(i+2)//2
        if i%2 == 0:
            if tone[j%7] == 'C' and j!=0:
                o+=1
            text = tone[j%7] + str(o)
        else:
            if tone[(j-4)%7] == 'C' and j!=0:
                o+=1
            text = tone[(j-4)%7] + str(o)
        if s == 0:text += '-'
        elif s == 2:text += '+'
        else:text = ' '+ text
        hex((cx,cy),N,skin[s])
        img = AddText(img,text,(cx-20,cy),textSize=52)
        print(text)


    
#cv2.imshow('img', img)
cv2.imwrite('key.png',img)
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
