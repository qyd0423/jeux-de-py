from cell import *
from settings import *
class Snake(object):
    '<=========~~'
    def __init__(self,game,x,y,body_length,direction,speed,skin_color,body_color,head_color,live=100):
        self.game = game
        self.field = self.game.field
        self.skin_color = skin_color
        self.body_color = body_color
        self.head_color = head_color
        self.head = Cell(x,y,self.skin_color,self.head_color)
        self.field.put_cell(self.head)
        tmp_body_cell = Cell(-1,-1,self.skin_color,self.body_color)
        self.body= [tmp_body_cell]*body_length
        self.direction = direction
        self.new_direction = direction
        self.speed = speed
        self.alive = True
        self.live = live
        self.sound_hit = pygame.mixer.Sound("C:\\Users\\qyd04\\Desktop\\tanchishe\\snake\\resourses\\hit.wav")
        self.sound_eat = pygame.mixer.Sound("C:\\Users\\qyd04\\Desktop\\tanchishe\\snake\\resourses\\eat.wav")

    def turn(self, **kwargs):
        if (self.direction in [LEFT,RIGHT] and
                    kwargs['direction'] in [UP, DOWN] or
                    self.direction in [UP,DOWN] and
                    kwargs['direction'] in [LEFT, RIGHT]):
            self.new_direction = kwargs['direction']

    def move(self):

        if self.alive:
            #改变方向
            self.direction = self.new_direction

            #探测下一个位置的物体
            meeting = self.field.get_cell(self.head.x + self.direction[0],
                                          self.head.y + self.direction[1])

            #死亡审判
            if meeting and meeting is not self.game.apple:
                self.die()
                return

            #判断是否吃了苹果，吃了就不断尾巴
            if meeting is self.game.apple:
                self.sound_eat.play()
                self.game.apple.drop()
                self.game.apple_counter += 1
                #print('吃了{}个苹果'.format(self.game.apple_counter))
            else:
                self.body,tail = self.body[:-1],self.body[-1]
                self.field.del_cell(tail.x,tail.y)

            #增加新的一节
            new_body_cell = Cell(self.head.x,self.head.y,
                                 self.skin_color,self.body_color)
            self.body = [new_body_cell] + self.body
            self.field.put_cell(new_body_cell)

            #移动蛇头
            self.head.move(*self.direction) #解包
            self.field.put_cell(self.head)

    def set_speed(self,speed): #设定速度
        self._speed = speed
        interval = 1000/self._speed
        self.game.add_update_action('snake.move',self.move,interval)
        #print('速度：{}'.format(self.speed))
    def get_speed(self): #获得速度
        return self._speed

    speed = property(get_speed,set_speed)

    def speed_up(self):
        if self.speed < 20:
            self.speed += 1

    def speed_down(self):
        if self.speed > 1:
            self.speed -= 1

    def die(self):
        import time
        time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        score='    '+str(self.game.apple_counter)+'           '
        output=open('resourses/snakeScore.txt','a')
        output.write(score)
        output.write(time+'\n')
        output.close()
        self.sound_hit.play()
        self.alive = False
        print('游戏结束')
        for body_cell in self.body:
            body_cell.color1 = SNAKE_COLOR_SKIN_D
            body_cell.color2 = SNAKE_COLOR_BODY_D
        self.head.color1 = SNAKE_COLOR_SKIN_D
        self.head.color2 = SNAKE_COLOR_HEAD_D


    def respawn(self):
        #复活
        if not self.alive:

            self.head = Cell(SNAKE_DEFAULT_X,SNAKE_DEFAULT_Y,
                             self.skin_color,self.head_color)
            self.field.put_cell(self.head)
            tmp_body_cell = Cell(-1, -1, self.skin_color, self.body_color)
            self.body = [tmp_body_cell] * SNAKE_DEFAULT_BODY_LENGTH
            self.direction = SNAKE_DEFAULT_DIRECTION
            self.new_direction = SNAKE_DEFAULT_DIRECTION
            self.speed = SNAKE_DEFAULT_SPEED
            self.alive = True
            self.live = SNAKE_DEFAULT_LIFE
