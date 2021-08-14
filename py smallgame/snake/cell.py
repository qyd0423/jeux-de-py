#-*- coding:utf-8 -*-

class Cell(object):
    """方块类"""

    def __init__(self,x,y,color1,color2): #初始化颜色，初始坐标
        self.x,self.y = x,y #初始坐标
        self.color1,self.color2 = color1,color2 #颜色

    def move(self,dx,dy): #方块移动
        self.x += dx
        self.y += dy

