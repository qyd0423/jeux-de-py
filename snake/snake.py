#-*- coding:utf-8 -*-

from mygame import *
from field import *
from asnake import *
from apple import  *


class snake(MyGame):

    def __init__(self):
        super(snake, self).__init__(GAME_NAME,SCREEN_SIZE,FPS,
                                    'resourses/MC.ttf',25,'resourses/pysnake.png')#初始父类
        self.background.fill(COLOR_BACKGROUND) #涂上底色
        for _ in range(CELL_SIZE,SCREEN_WIDTH,CELL_SIZE):
            pygame.draw.line(self.background,COLOR_LINE,
                             (_,0),(_,SCREEN_HEIGHT))
        for _ in range(CELL_SIZE, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.background, COLOR_LINE,
                             (0, _), (SCREEN_WIDTH, _))

        self.field = Field(self,COLUMNS,ROWS)
        self.apple_counter = 0
        self.apple = Apple(self)
        self.snake = Snake(self,SNAKE_DEFAULT_X,SNAKE_DEFAULT_Y,
                           SNAKE_DEFAULT_BODY_LENGTH,SNAKE_DEFAULT_DIRECTION,
                           SNAKE_DEFAULT_SPEED,
                           SNAKE_COLOR_SKIN,SNAKE_COLOR_BODY,SNAKE_COLOR_HEAD)
        #控制按键设定
        self.key_bind(KEY_EXIT,self.quit)
        self.key_bind(KEY_UP, self.snake.turn,direction=UP)
        self.key_bind(KEY_DOWN, self.snake.turn,direction=DOWN)
        self.key_bind(KEY_LEFT, self.snake.turn,direction=LEFT)
        self.key_bind(KEY_RIGHT, self.snake.turn,direction=RIGHT)
        self.key_bind(pygame.K_EQUALS, self.snake.speed_up)
        self.key_bind(pygame.K_MINUS, self.snake.speed_down)
        self.key_bind(KEY_RESPAWN, self.restart)
        self.key_bind(pygame.K_g, self.show_score)

        self.add_draw_action(self.show)

    def restart(self):
        if not self.snake.alive:
            self.field.clear()  # 移除尸体
            self.apple_counter = 0 #重新计数
            self.apple.drop()
            self.snake.respawn()

    def show_score(self):
        score=[]


    def show(self):
        text = "Score: %d"% self.apple_counter
        output = self.font.render(text,True,(255,255,33))
        self.screen.blit(output,(0,0))

        text = "Speed: %d" % self.snake.speed
        output = self.font.render(text, True, (255, 255, 33))
        self.screen.blit(output, (500, 0))
        if not self.snake.alive:
            text = ' GAME OVER '
            output = self.font.render(text,True,(255,33,33),WHITE)
            self.screen.blit(output,(320-84, 120))
            text = '  Press  R  to  restart  '
            output = self.font.render(text, True, BLACK,LIGHT_GREY)
            self.screen.blit(output, (320 - 150, 150))
            output = open('resourses/snakeScore.txt', 'r')
            l=0
            for line in output:
                output = pygame.font.Font('resourses/MC.ttf', 16).render(line, True, BLACK)
                self.screen.blit(output, (320-150,190+l))
                l+=35
        if not self.running and self.snake.alive:
            text = " Press SPACE to start"
            output = self.font.render(text, True, GREY, LIGHT_GREY)
            self.screen.blit(output,(320-160, 240-10))

if __name__ == '__main__':
    snake().run()