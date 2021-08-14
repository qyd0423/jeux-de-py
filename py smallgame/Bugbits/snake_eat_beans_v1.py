#!/usr/bin/env python
from typing import List

import pygame, sys, time, random, os
from pygame.locals import *
import game
# 定义界面大小
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
GRID_SIZE = 20

# 定义蛇相关常数
SNAKE_INIT_LEN = 3
SNAKE_INIT_POS_MARGIN = 5
SNAKE_VEL_SLOW = 1
SNAKE_VEL_FAST = 2
SNAKE_ACC_TIME = 50

# 定义豆子数量
BEAN_NUM = 30

# 定义颜色变量
RED = pygame.Color(255, 0, 0)
RED_HEAD = pygame.Color(255, 150, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(150, 150, 150)
GREEN = pygame.Color(0, 255, 0)
GREEN_HEAD = pygame.Color(100, 200, 200)
YELLOW = pygame.Color(255, 255, 0)
BLUE = pygame.Color(0, 0, 255)

NORMAL_BEAN_COLOR = YELLOW


class Snake:
    def __init__(self, color, headColor, ctrlKeys):
        self.color = color
        self.headColor = headColor
        self.ctrlKeys = ctrlKeys  # 按[上，下，左，右，加速]的顺序
        self.vel = SNAKE_VEL_SLOW
        self.velCount = 0
        self.segments = []
        self.generate()

    def handleKey(self, pressKey):
        directions = [-2, 2, -1, 1]  # ([-2,2,-1,1]) # 方向[-2,2,-1,1]分别表示[上，下，左，右]
        for direct, key in zip(directions, self.ctrlKeys[:4]):
            if key == pressKey and direct + self.direction != 0:
                self.direction = direct
        if pressKey == self.ctrlKeys[4] and self.vel != SNAKE_VEL_FAST:  # 按下了加速键
            if self.getLen() > SNAKE_INIT_LEN:
                self.pop()  # 燃烧自己
                self.vel = SNAKE_VEL_FAST  # 来加速
                self.velCount = SNAKE_ACC_TIME

    def moveAndAdd(self, snake=[]):
        # 根据方向移动蛇头的坐标
        if self.direction == 1:
            self.headPos[0] += GRID_SIZE
        if self.direction == -1:
            self.headPos[0] -= GRID_SIZE
        if self.direction == -2:
            self.headPos[1] -= GRID_SIZE
        if self.direction == 2:
            self.headPos[1] += GRID_SIZE
        # 检查蛇头是否撞到另一条蛇身
        if snake == []:
            self.segments.insert(0, list(self.headPos))  # 在蛇头插入一格
            if self.velCount > 0:
                self.velCount = self.velCount - 1
            else:
                self.vel = SNAKE_VEL_SLOW
            return False
        isSnakeHit = False
        for pos in snake.segments:
            if self.headPos == pos:
                isSnakeHit = True
                break
        if not isSnakeHit:
            self.segments.insert(0, list(self.headPos))  # 在蛇头插入一格
            if self.velCount > 0:
                self.velCount = self.velCount - 1
            else:
                self.vel = SNAKE_VEL_SLOW
        return isSnakeHit

    def pop(self):
        self.segments.pop()  # 在蛇尾减去一格

    def show(self, playSurface):
        # 画蛇身
        for pos in self.segments[1:]:
            pygame.draw.rect(playSurface, self.color, Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))
        # 画蛇头
        pygame.draw.rect(playSurface, self.headColor, Rect(self.headPos[0], self.headPos[1], GRID_SIZE, GRID_SIZE))

    def generate(self):
        x = random.randrange(SNAKE_INIT_POS_MARGIN, SCREEN_WIDTH / GRID_SIZE - SNAKE_INIT_POS_MARGIN)
        y = random.randrange(SNAKE_INIT_POS_MARGIN, SCREEN_HEIGHT / GRID_SIZE - SNAKE_INIT_POS_MARGIN)
        self.direction = random.choice([-2, 2, -1, 1])  # ([-2,2,-1,1]) # 方向[-2,2,-1,1]分别表示[上，下，左，右]
        self.headPos = [int(x * GRID_SIZE), int(y * GRID_SIZE)]
        self.segments.clear()
        self.segments.insert(0, list(self.headPos))
        for i in range(SNAKE_INIT_LEN - 1):
            self.moveAndAdd()

    def respawn(self, normalBeanss=[], snakeBeanss=[], snakes=[]):
        self.generate()
        while not isEmptyInArea(self.segments, normalBeanss, snakeBeanss, snakes):
            self.generate()
        self.vel = SNAKE_VEL_SLOW
        self.velCount = 0

    def isDead(self):
        if self.headPos[0] > SCREEN_WIDTH - GRID_SIZE or self.headPos[0] < 0 or self.headPos[
            1] > SCREEN_HEIGHT - GRID_SIZE or self.headPos[1] < GRID_SIZE:
            return True
        return False

    def getLen(self):
        return len(self.segments)


class Bean:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    def beEaten(self, snakePos):
        if snakePos[0] == self.pos[0] and snakePos[1] == self.pos[1]:
            return True
        else:
            return False


class NormalBeans:
    def __init__(self, color, totalNum):
        self.color = color
        self.totalNum = totalNum
        self.curNum = 0
        self.beans = []

    def generate(self, snakeBeanss, snakes):
        while self.curNum < self.totalNum:
            x = random.randrange(0, SCREEN_WIDTH / GRID_SIZE)
            y = random.randrange(1, SCREEN_HEIGHT / GRID_SIZE)
            newBeanPos = [int(x * GRID_SIZE), int(y * GRID_SIZE)]
            # 检查豆子位置是否重复
            if isEmptyInArea([newBeanPos], [self], snakeBeanss, snakes):
                # 新生成的豆子在不重复的地方
                self.beans.append(Bean(self.color, newBeanPos))
                self.curNum = self.curNum + 1

    def beEaten(self, snakePos):
        for bean in self.beans:
            if bean.beEaten(snakePos):
                self.beans.remove(bean)
                self.curNum = self.curNum - 1
                return True
        return False

    def show(self, playSurface):
        for bean in self.beans:
            pygame.draw.rect(playSurface, self.color, Rect(bean.pos[0], bean.pos[1], GRID_SIZE, GRID_SIZE))


class SnakeBeans:
    def __init__(self, snake):
        self.color = NORMAL_BEAN_COLOR
        self.beans = []
        for pos in snake.segments:
            self.beans.append(Bean(NORMAL_BEAN_COLOR, pos))

    def beEaten(self, snakePos):
        for bean in self.beans:
            if bean.beEaten(snakePos):
                self.beans.remove(bean)
                return True
        return False

    def show(self, playSurface):
        for bean in self.beans:
            pygame.draw.rect(playSurface, self.color, Rect(bean.pos[0], bean.pos[1], GRID_SIZE, GRID_SIZE))


def isEmptyInArea(area, normalBeanss=[], snakeBeanss=[], snakes=[]):
    ''' area是位置的列表
    '''
    for pos in area:
        if normalBeanss != []:
            for nbs in normalBeanss:
                for nb in nbs.beans:
                    if nb.pos == pos:
                        return False
        if snakeBeanss != []:
            for sbs in snakeBeanss:
                if sbs != []:
                    for sb in sbs.beans:
                        if sb.pos == pos:
                            return False

    return True


def play_single_game():
    pygame.init()
    fpsClock = pygame.time.Clock()
    # 创建pygame显示层
    playSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Eat Beans')
    # 分数显示层字体大小
    scoreFont = pygame.font.Font("D:\\pythonex\\snake\\font\\comici.ttf", 32)

    # 初始化蛇
    ctrlKeys2 = [K_UP, K_DOWN, K_LEFT, K_RIGHT, ord('m')]
    snake2 = Snake(RED, RED_HEAD, ctrlKeys2)
    snake2VelCount = 1

    # 初始化豆子
    snake2Beans = []
    normBeans = NormalBeans(NORMAL_BEAN_COLOR, BEAN_NUM)
    normBeans.generate(snake2Beans, snake2)

    while True:
        # 检测按键等pygame事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                play()
                # sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                else:
                    snake2.handleKey(event.key)

        # 根据方向移动蛇并增加蛇长度一格
        if snake2VelCount > 1:
            if snake2.moveAndAdd():  # 撞到了另一条蛇身
                snake2Beans = SnakeBeans()
                snake2.respawn([normBeans], snake2Beans, snake2)
                continue

        # 判断是否有豆子被吃，如果没有任何豆子被吃掉，蛇长度减少一格
        if snake2VelCount > 1:
            isAnyBeanEaten = False
            if normBeans.beEaten(snake2.headPos):
                normBeans.generate(snake2Beans, snake2)  # 如果普通豆子被吃掉，则重新生成豆子
                isAnyBeanEaten = True
            if snake2Beans != [] and snake2Beans.beEaten(snake2.headPos):
                isAnyBeanEaten = True
            if not isAnyBeanEaten:
                snake2.pop()

        # 绘制刷新
        playSurface.fill(BLACK)  # 绘制pygame显示层
        normBeans.show(playSurface)
        snake2.show(playSurface)
        if snake2Beans != []:
            snake2Beans.show(playSurface)
        # 显示分数
        scoreSurf = scoreFont.render('P1 Score:{}'.format(snake2.getLen() - SNAKE_INIT_LEN), True,
                                     WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.midtop = (SCREEN_WIDTH / 2, 0)
        playSurface.blit(scoreSurf, scoreRect)
        pygame.display.flip()  # 刷新pygame显示层

        # 若死亡则重生
        if snake2VelCount > 1:
            if snake2.isDead():
                snake2.respawn([normBeans], snake2Beans, snake2)

        if snake2VelCount > 1:
            if snake2.vel == SNAKE_VEL_FAST:
                snake2VelCount = 2
            else:
                snake2VelCount = 1
        else:
            snake2VelCount = snake2VelCount + 1

        # 控制游戏速度
        fpsClock.tick(10)


def play_double_game():
    pygame.init()
    fpsClock = pygame.time.Clock()
    # 创建pygame显示层
    playSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Eat Beans')
    # 分数显示层字体大小
    scoreFont = pygame.font.Font("D:\\pythonex\\snake\\font\\comici.ttf", int(32 * GRID_SIZE / 20))

    # 初始化蛇
    ctrlKeys1 = [ord('w'), ord('s'), ord('a'), ord('d'), ord('g')]
    ctrlKeys2 = [K_UP, K_DOWN, K_LEFT, K_RIGHT, ord('m')]
    snake1 = Snake(GREEN, GREEN_HEAD, ctrlKeys1)
    snake2 = Snake(RED, RED_HEAD, ctrlKeys2)
    snake1VelCount = 1
    snake2VelCount = 1

    # 初始化豆子
    snake1Beans = []
    snake2Beans = []
    normBeans = NormalBeans(NORMAL_BEAN_COLOR, BEAN_NUM)
    normBeans.generate([snake1Beans, snake2Beans], [snake1, snake2])

    while True:
        # 检测按键等pygame事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                play()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                else:
                    snake1.handleKey(event.key)
                    snake2.handleKey(event.key)

        # 根据方向移动蛇并增加蛇长度一格
        if snake1VelCount > 1:
            if snake1.moveAndAdd(snake2):  # 撞到了另一条蛇身
                snake1Beans = SnakeBeans(snake1)
                snake1.respawn([normBeans], [snake1Beans, snake2Beans], [snake2])
                continue
        if snake2VelCount > 1:
            if snake2.moveAndAdd(snake1):  # 撞到了另一条蛇身
                snake2Beans = SnakeBeans(snake2)
                snake2.respawn([normBeans], [snake1Beans, snake2Beans], [snake1])
                continue

        # 判断是否有豆子被吃，如果没有任何豆子被吃掉，蛇长度减少一格
        if snake1VelCount > 1:
            isAnyBeanEaten = False
            if normBeans.beEaten(snake1.headPos):
                normBeans.generate([snake1Beans, snake2Beans], [snake1, snake2])  # 如果普通豆子被吃掉，则重新生成豆子
                isAnyBeanEaten = True
            if snake1Beans != [] and snake1Beans.beEaten(snake1.headPos):
                isAnyBeanEaten = True
            if snake2Beans != [] and snake2Beans.beEaten(snake1.headPos):
                isAnyBeanEaten = True
            if not isAnyBeanEaten:
                snake1.pop()
        if snake2VelCount > 1:
            isAnyBeanEaten = False
            if normBeans.beEaten(snake2.headPos):
                normBeans.generate([snake1Beans, snake2Beans], [snake1, snake2])  # 如果普通豆子被吃掉，则重新生成豆子
                isAnyBeanEaten = True
            if snake1Beans != [] and snake1Beans.beEaten(snake2.headPos):
                isAnyBeanEaten = True
            if snake2Beans != [] and snake2Beans.beEaten(snake2.headPos):
                isAnyBeanEaten = True
            if not isAnyBeanEaten:
                snake2.pop()

        # 绘制刷新
        playSurface.fill(BLACK)  # 绘制pygame显示层
        normBeans.show(playSurface)
        snake1.show(playSurface)
        snake2.show(playSurface)
        if snake1Beans != []:
            snake1Beans.show(playSurface)
        if snake2Beans != []:
            snake2Beans.show(playSurface)
        # 显示分数
        scoreSurf = scoreFont.render('P1 Score:{}    vs    P2 Score:{}'.format(snake1.getLen() - SNAKE_INIT_LEN,
                                                                               snake2.getLen() - SNAKE_INIT_LEN), True,
                                     WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.midtop = (SCREEN_WIDTH / 2, 0)
        playSurface.blit(scoreSurf, scoreRect)
        pygame.display.flip()  # 刷新pygame显示层

        # 若死亡则重生
        if snake1VelCount > 1:
            if snake1.isDead():
                snake1.respawn([normBeans], [snake1Beans, snake2Beans], [snake2])
        if snake2VelCount > 1:
            if snake2.isDead():
                snake2.respawn([normBeans], [snake1Beans, snake2Beans], [snake1])

        if snake1VelCount > 1:
            if snake1.vel == SNAKE_VEL_FAST:
                snake1VelCount = 2
            else:
                snake1VelCount = 1
        else:
            snake1VelCount = snake1VelCount + 1

        if snake2VelCount > 1:
            if snake2.vel == SNAKE_VEL_FAST:
                snake2VelCount = 2
            else:
                snake2VelCount = 1
        else:
            snake2VelCount = snake2VelCount + 1

        # 控制游戏速度
        fpsClock.tick(10)


def play():
    mode = input(('''        
    P1操作说明：↑↓←→
    P2操作说明，wsad
    ESC回到菜单

    请选择模式  
        1、单人游戏
        2、双人对战 
        0、退出游戏  
    '''))
    if mode == "1":
        play_single_game()
    elif mode == "2":
        play_double_game()
    elif mode == "0":
        #exit()
        game.start_game()
    else:
        print("ERROR")


if __name__ == "__main__":
    while True:
        play()
