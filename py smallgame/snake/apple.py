#-*- coding:utf-8 -*-

from settings import *
from cell import *
from random import *

class Apple(Cell):
    '食物'

    def __init__(self,game):
        super(Apple, self).__init__(0,0,APPLE_COLOR1,APPLE_COLOR2)
        self.field = game.field
        self.drop()

    def drop(self):
        while True:
            x,y = randint(0,COLUMNS-1),randint(0,ROWS-1)
            #确保苹果不落在蛇身上
            if self.field.get_cell(x,y) is None:
                self.x,self.y = x,y
                self.field.put_cell(self)
                break