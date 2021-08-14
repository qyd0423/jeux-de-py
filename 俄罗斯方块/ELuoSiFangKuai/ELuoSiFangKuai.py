from tkinter import *
from time import sleep
from random import *
from tkinter import messagebox

class Teris:
    def __init__(self):
        # 方块颜色列表
        self.color = ['red', 'orange', 'yellow', 'purple', 'blue', 'green', 'pink']
        # 设置核心方块，任何形状都可以通过相对位置绘制
        # 字典 存储形状对应7种形状 元组存储坐标
        self.shapeDict = {1: [(0, 0), (0, -1), (0, -2), (0, 1)],  # 方块 I 型
                          2: [(0, 0), (0, -1), (1, -1), (1, 0)],  # 方块 O  型
                          3: [(0, 0), (-1, 0), (0, -1), (1, 0)],  # 方块 T 型
                          4: [(0, 0), (0, -1), (1, 0), (2, 0)],  # 方块 J 右长倒L盖子型
                          5: [(0, 0), (0, -1), (-1, 0), (-2, 0)],  # 方块 L 型
                          6: [(0, 0), (0, -1), (-1, -1), (1, 0)],  # 方块 Z 型
                          7: [(0, 0), (-1, 0), (0, -1), (1, -1)]}  # 方块 S 型
        # 旋转坐标控制
        self.rotateDict = {(0, 0): (0, 0), (0, 1): (-1, 0), (0, 2): (-2, 0), (0, -1): (1, 0),
                           (0, -2): (2, 0), (1, 0): (0, 1), (2, 0): (0, 2), (-1, 0): (0, -1),
                           (-2, 0): (0, -2), (1, 1): (-1, 1), (-1, 1): (-1, -1),
                           (-1, -1): (1, -1), (1, -1): (1, 1)}
        # 初始高度，宽度 核心块位置
        self.coreLocation = [4, -2]
        self.height, self.width = 20, 10
        self.size = 32
        # Map can record the location of every square.i宽  j高
        self.map = {}
        # 全部置0
        for i in range(self.width):
            for j in range(-4, self.height):
                self.map[(i, j)] = 0
        # 添加边界
        for i in range(-4, self.width + 4):
            self.map[(i, self.height)] = 1
        for j in range(-4, self.height + 4):
            for i in range(-4, 0):
                self.map[(i, j)] = 1
        for j in range(-4, self.height + 4):
            for i in range(self.width, self.width + 4):
                self.map[(i, j)] = 1

        # 初始化分数0  默认不加快  按下时加快
        self.score = 0
        self.isFaster = False
        # 创建GUI界面
        self.root = Tk()
        self.root.title("俄罗斯方块2.0")
        self.root.geometry("500x645")
        self.area = Canvas(self.root, width=320, height=640, bg='black')
        self.area.grid(row=2)
        self.pauseBut = Button(self.root, text="暂停", height=2, width=13, font=(18), command=self.isPause)
        self.pauseBut.place(x=340, y=100)
        self.startBut = Button(self.root, text="开始", height=2, width=13, font=(18), command=self.play)
        self.startBut.place(x=340, y=20)
        self.restartBut = Button(self.root, text="重新开始", height=2, width=13, font=(18), command=self.isRestart)
        self.restartBut.place(x=340, y=180)
        self.quitBut = Button(self.root, text="退出", height=2, width=13, font=(18), command=self.isQuit)
        self.quitBut.place(x=340, y=260)
        self.scoreLabel1 = Label(self.root, text="分数:", font=(24))
        self.scoreLabel1.place(x=340, y=600)
        self.scoreLabel2 = Label(self.root, text="0", fg='red', font=(24))
        self.scoreLabel2.place(x=410, y=600)
        # 按键交互
        self.area.bind("<Up>", self.rotate)
        self.area.bind("<Left>", self.moveLeft)
        self.area.bind("<Right>", self.moveRight)
        self.area.bind("<Down>", self.moveFaster)
        self.area.bind("<Key-w>", self.rotate)
        self.area.bind("<Key-a>", self.moveLeft)
        self.area.bind("<Key-d>", self.moveRight)
        self.area.bind("<Key-s>", self.moveFaster)
        self.area.focus_set()
        # 菜单
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.startMenu = Menu(self.menu)
        self.menu.add_cascade(label='开始', menu=self.startMenu)
        self.startMenu.add_command(label='开始新的游戏', command=self.isRestart)
        self.startMenu.add_separator()
        self.startMenu.add_command(label='重置当前方块', command=self.play)
        self.exitMenu = Menu(self.menu)
        self.menu.add_cascade(label='退出', command=self.isQuit)
        self.helpMenu = Menu(self.root)
        self.menu.add_cascade(label='帮助', menu=self.helpMenu)
        self.helpMenu.add_command(label='玩法介绍', command=self.rule)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label='关于', command=self.about)

    # 先将核心块的所在位置在map中的元素设为1，通过self.shapeDict获取其余方块位置，将map中对应元素设为1。
    def getLocation(self):
        map[(core[0], core[1])] = 1
        for i in range(4):
            map[((core[0] + getNew[i][0]),
                 (core[1] + getNew[i][1]))] = 1

    # 判断方块下移一格后对应位置map中的元素是否为一，是，则不可移动，返回False；否，可以移动，返回True。
    def canMove(self):
        for i in range(4):
            if map[(core[0] + getNew[i][0]), (core[1] + 1 + getNew[i][1])] == 1:
                return False
        return True

    # 先用randRange获取1～7中的随机整数，随机到某一整数，那么访问self.shapeDict,获取这种形状方块的核心块及其他方块的相对位置。
    # 访问颜色字典，获取此方块的颜色。建立循环，当方块可移动时(while self. canMove():)，且暂停键未被摁下（if isPause:)，
    # 核心块纵坐标加一，根据核心块及其他方块对于核心块的相对位置，画出四个方块。用self.getLocation()函数获取方块的位置。
    def drawNew(self):
        global next
        global getNew
        global core
        next = randrange(1, 8)
        # 形状
        self.getNew = self.shapeDict[next]
        getNew = self.getNew
        core = [4, -2]
        time = 0.2
        while self.canMove():
            if isPause:
                core[1] += 1
                self.drawSquare()
                if self.isFaster:
                    sleep(time - 0.15)
                else:
                    sleep(time + 0.22)
                self.isFaster = False
            else:
                self.drawSquare()
                sleep(time)
        self.getLocation()

    # 绘制当前方块
    def drawSquare(self):
        self.area.delete("new")
        for i in range(4):
            self.area.create_rectangle((core[0] + self.getNew[i][0]) * self.size,
                                       (core[1] + self.getNew[i][1]) * self.size,
                                       (core[0] + self.getNew[i][0] + 1) * self.size,
                                       (core[1] + self.getNew[i][1] + 1) * self.size,
                                       fill=self.color[next - 1], tags="new")
        self.area.update()

    # 给底部每行中方块都加上标签：bottom + str(j), j代表该块所在行数
    def drawBottom(self):
        for j in range(self.height):
            self.area.delete('bottom' + str(j))
            for i in range(self.width):
                if map[(i, j)] == 1:
                    self.area.create_rectangle(self.size * i, self.size * j, self.size * (i + 1),
                                               self.size * (j + 1), fill='grey', tags='bottom' + str(j))
                                                # 此处设定底部方块颜色
            self.area.update()

    # 判断填满遍历每一行的各个元素的map值
    def isFill(self):
        for j in range(self.height):
            t = 0
            for i in range(self.width):
                if map[(i, j)] == 1:
                    t = t + 1
            if t == self.width:
                self.getScore()
                self.deleteLine(j)

    # 加分
    def getScore(self):
        scoreValue = eval(self.scoreLabel2['text'])
        scoreValue += 10
        self.scoreLabel2.config(text=str(scoreValue))

    # 消行
    def deleteLine(self, j):
        for t in range(j, 2, -1):
            for i in range(self.width):
                map[(i, t)] = map[(i, t - 1)]
        for i in range(self.width):
            map[(i, 0)] = 0
        self.drawBottom()

    # 判断方块上顶溢出结束游戏
    def isOver(self):
        t = 0
        for j in range(self.height):
            for i in range(self.width):
                if self.map[(i, j)] == 1:
                    t += 1
                    break
        if t >= self.height:
            return False
        else:
            return True

    # 判断旋转
    def canRotate(self):
        for i in range(4):
            map[((core[0] + getNew[i][0]),
                 (core[1] + getNew[i][1]))] = 0
        for i in range(4):
            if map[((core[0] + self.rotateDict[getNew[i]][0]),
                    (core[1] + self.rotateDict[getNew[i]][1]))] == 1:
                return False
        return True

    # 旋转
    def rotate(self, event):
        if next != 2:
            if self.canRotate():
                for i in range(4):
                    getNew[i] = self.rotateDict[getNew[i]]
                self.drawSquare()
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1
    # 判断左移
    def canLeft(self):
        coreNow = core
        for i in range(4):
            map[((coreNow[0] + getNew[i][0]), (coreNow[1] + getNew[i][1]))] = 0
        for i in range(4):
            if map[((coreNow[0] + getNew[i][0] - 1), (coreNow[1] + getNew[i][1]))] == 1:
                return False
        return True

    # 左移
    def moveLeft(self, event):
        if self.canLeft():
            core[0] -= 1
            self.drawSquare()
            self.drawBottom()
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1

    # 判断右移
    def canRight(self):
        for i in range(4):
            map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 0
        for i in range(4):
            if map[((core[0] + getNew[i][0] + 1), (core[1] + getNew[i][1]))] == 1:
                return False
        return True

    # 右移
    def moveRight(self, event):
        if self.canRight():
            core[0] += 1
            self.drawSquare()
            self.drawBottom()
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1

    # 初始化中有一self. isFaster 的变量被设为False，当其为False时，
    # 程序中的sleep(time)中time的值为0.35，而按下下键，self. isFaster变为True，
    # time变成0.05，通过调整sleep()中变量的大小可以调节方块运动的速度。
    # 此功能通过if语句实现。
    def moveFaster(self, event):
        self.isFaster = True
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1

    # 运行程序
    def run(self):
        self.isFill()
        self.drawNew()
        self.drawBottom()

    # 开始游戏
    def play(self):
        self.startBut.config(state=DISABLED)
        global isPause
        isPause = True
        global map
        map = self.map
        while True:
            if self.isOver():
                self.run()
            else:
                break
        self.over()

    # 重新开始游戏
    def restart(self):
        self.core = [4, -2]
        self.map = {}
        for i in range(self.width):
            for j in range(-4, self.height):
                self.map[(i, j)] = 0
        for i in range(-1, self.width):
            self.map[(i, self.height)] = 1
        for j in range(-4, self.height + 1):
            self.map[(-1, j)] = 1
            self.map[(self.width, j)] = 1
        self.score = 0
        self.t = 0.07
        for j in range(self.height):
            self.area.delete('bottom' + str(j))
        self.play()

    # 结束后告诉用户失败
    def over(self):
        feedback = messagebox.askquestion("你失败了!", "你失败了!\n要重新开始吗?")
        if feedback == 'yes':
            self.restart()
        else:
            self.root.destroy()

    # 退出
    def isQuit(self):
        askQuit = messagebox.askquestion("退出", "你确定要退出游戏吗?")
        if askQuit == 'yes':
            self.root.destroy()
            exit()

    # 判断是否按下“重新开始”按钮
    def isRestart(self):
        askRestart = messagebox.askquestion("重新开始", "你确定要重新开始吗?")
        if askRestart == 'yes':
            self.restart()
        else:
            return

    # 每次一按下暂停键，isPause = not isPause,当isPause = True时，由于之前提到过的if isPause:语句，
    # 方块可以移动，游戏运行。当按下暂停键以后，isPause值为False，方块将不可移动。同时，isPause值为False时
    # ，暂停键变为开始键，即标签由Pause 改为 Resume,当isPause值为True时，Resume改为Pause。这一功能由if语句实现。
    def isPause(self):
        global isPause
        isPause = not isPause
        if not isPause:
            self.pauseBut["text"] = "恢复"
        else:
            self.pauseBut["text"] = "暂停"

    # 帮助
    def rule(self):
        ruleTop = Toplevel()
        ruleTop.title('帮助')
        ruleTop.geometry('1000x200')
        rule = "点击’开始‘按钮开始游戏；\n\
        重置当前方块: 点击按钮使当前下坠方块回到上方并重新下落；\n\
        游戏中使用键盘方向键←、→控制左右移动，键盘方向键↑进行变形，键盘方向↓加速下落。\n\
         have fun!"
        ruleLabel = Label(ruleTop, text=rule, fg='blue', font=(18))
        ruleLabel.place(x=50, y=50)

    # 显示有关信息
    def about(self):
        aboutTop = Toplevel()
        aboutTop.title('关于本程序')
        aboutTop.geometry('300x150')
        about = "本程序仅供学习\n\
               借鉴了某些网上的思路\n\
               可能是一次失败的大作业"
        aboutLabel = Label(aboutTop, font=('Curier', 20), fg='darkblue', text=about)
        aboutLabel.pack()

    # 进入到事件（消息）循环
    def mainloop(self):
        self.root.mainloop()
# 运行主程序
def main():
    teris = Teris()
    teris.mainloop()
main()