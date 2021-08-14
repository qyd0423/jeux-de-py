#-*- coding:utf-8 -*-

import sys
import pygame

class MyGame(object):
    "pygame模板类"
    def __init__(self,name='My Game',size=(640,480),fps=60,
                 font_filename='MC.ttf',font_size = 16,icon=None):
        pygame.init()
        pygame.mixer.init() #音乐
        self.sound_pause = pygame.mixer.Sound('resourses/pause.wav')
        pygame.display.set_caption(name) #窗口标题
        self.screen_size = self.screen_width,self.screen_height = size #窗口大小
        pygame.display.set_icon(pygame.image.load(icon)) if icon else None  # 三元操作符,加载窗口图标
        self.screen = pygame.display.set_mode(self.screen_size) #生成窗口
        self.fps = fps #更新频率
        self.font = pygame.font.Font(font_filename,font_size)
        self.clock = pygame.time.Clock()
        self.now = 0 #当前游戏时间
        self.background = pygame.Surface(self.screen_size)
        self.key_event_binds = {} #键和函数绑定的字典
        self.gamedata_update_actions = {} #游戏事件字典
        self.display_update_actions = [self.draw_background] # 游戏动作,需要有固定顺序
        self.running = True
        self.key_bind(pygame.K_SPACE,self.switch_running)

    def draw_background(self):
        self.screen.blit(self.background,(0,0))

    def run(self):
        self.switch_running()
        while True:
            self.now = pygame.time.get_ticks()  # 获取游戏时间
            self._process_events() #处理事件
            if self.running:
                self._update_gamedata() #更新数据
            self._update_display() #更新画面
            self.clock.tick(self.fps) #控制画面刷新频率

    def switch_running(self):
        self.sound_pause.play()
        self.running = not self.running
        if self.running:
            # 重新计时
            for name,action in self.gamedata_update_actions.items():
                if action['next_time']:
                    action['next_time'] = self.now + action['interval']

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                action,args = self.key_event_binds.get(event.key,
                                                       (None,None))
                action(**args) if args else action() if action else None #两个三元操作，**args将字典展开

    def _update_gamedata(self):
        for name,action in self.gamedata_update_actions.items():
            #下一次运行的时间等于当前时间+时间间隔
            if not action['next_time']:
                action['run']()
            elif self.now >= action['next_time']:
                action['next_time'] += action['interval']
                action['run']() #函数

    def _update_display(self):
        for action in self.display_update_actions: #执行该列表中的函数
            action()
        pygame.display.flip()

    def key_bind(self,key,action,**args):
        self.key_event_binds[key] = action,args

    def add_update_action(self,name,action,interval=0):
        next_time = self.now + interval if interval else None
        self.gamedata_update_actions[name] = dict(run=action,
                                                  interval=interval,
                                                  next_time=next_time)

    def add_draw_action(self,action):
        self.display_update_actions.append(action)

    def quit(self):
        pygame.quit()
        sys.exit(0)
