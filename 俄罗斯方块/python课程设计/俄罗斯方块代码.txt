from tkinter import *
import time
import threading
import random
import math
from tkinter import messagebox

# 变量定义
BIANCHANG = 19   #定义边长
COLOR = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', '#00C5CD', '#00EE76', '#388E8E', '#556B2F', '#6B8E23',
         '#8B2252', '#8B6969', '#A0522D', '#BC8F8F', '#BC8F3F', 'black']   #定义颜色
COLUMN = 16  #列数
ROW = 30  #行数

#定义方块类
class fangk:
    def __init__(self, huabu, col, row):   #属于对象的数据成员,
        self.huabu = huabu    #定义画布
        self.col, self.row = col, row #col-->第几行的行，row-->第几列的列
        self.color = COLOR[self.row % 16]#方块的颜色在这16中颜色中随机产生
        self.havefk = False #界面上有无方块的标志

    def setvisible(self, statu): #设置显示与否
        if statu > 0:
            x = self.col * (BIANCHANG + 1) + 2
            y = 582 - (ROW - self.row - 1) * (BIANCHANG + 1)
            self.fk = self.huabu.create_rectangle(x, y, x + BIANCHANG, y + BIANCHANG, fill=self.color)#画块
            #(creat_rectangle(x1,y1,x2,y2):画一个矩形(对角顶点坐标为(x1,y1),(x2,y2))
            self.line1 = self.huabu.create_line(x, y, x, y + BIANCHANG, fill='white')#边线加白#create_line() :画线
            self.line2 = self.huabu.create_line(x, y, x + BIANCHANG, y, fill='white')
            self.havefk = True
        elif statu == 0 and self.havefk:
            self.huabu.delete(self.fk)#detele()删除对变量的引用
            self.huabu.delete(self.line2)
            self.huabu.delete(self.line1)
            self.havefk = False
        else:
            return -1

    def set_color(self, color): #设置颜色
        self.color = color
        return self

#定义方块的各种形状 # 字典 存储形状对应7种形状 元组存储坐标
class elsfk:
    def __init__(self):
        self.fk_type = [[(0, 0, 1, 1), (0, 1, 0, 1)],  # 正方形
                        [(0, 0, 0, 0), (1, 0, -1, -2)],  # 长条
                        [(-1, 0, 1, 2), (0, 0, 0, 0)],
                        [(0, 1, 0, -1), (0, 1, 1, 0)],  # 右Z
                        [(0, -1, -1, 0), (0, 1, 0, -1)],
                        [(0, -1, 0, 1), (0, 1, 1, 0)],  # 左Z
                        [(0, 1, 1, 0), (0, 1, 0, -1)],
                        [(0, 0, -1, 1), (0, 1, 0, 0)],  # T型
                        [(0, 0, 0, 1), (0, 1, -1, 0)],
                        [(0, 1, 0, -1), (0, 0, -1, 0)],
                        [(0, 0, -1, 0), (0, 1, 0, -1)],
                        [(0, 1, 1, -1), (0, -1, 0, 0)],  # 左钩
                        [(0, 1, 0, 0), (0, 1, 1, -1)],
                        [(0, -1, -1, 1), (0, 1, 0, 0)],
                        [(0, 0, 0, -1), (0, 1, -1, -1)],
                        [(0, 1, 1, -1), (0, 1, 0, 0)],  # 右钩
                        [(0, -1, 0, 0), (0, 1, 1, -1)],
                        [(0, -1, -1, 1), (0, -1, 0, 0)],
                        [(0, 0, 0, 1), (0, 1, -1, -1)]]

# 窗口           
        self.win = Tk()#创建窗口
        self.win.title("俄罗斯方块")#窗口的名字
        # self.win.attributes("-alpha",0.95)
        self.win.geometry('450x610')
        self.win.resizable(0, 0)#窗口的长宽不可改变
        self.nandu_stat=IntVar() #让窗口运行起来
        self.huabu = Canvas(self.win, bg="light grey", height=600, width=COLUMN * (BIANCHANG + 1), takefocus=True)##方块下落画布
        self.huabu_right = Canvas(self.win, height=100, width=100) #下一个方块预览画布

        

#下面我们添加四个按钮，分别是开始、暂停、重新开始、退出。多个文本，比如：等级、分数，
        self.pauseBut = Button(self.win, text="暂停", bg='light green', height=1, width=12, font=(10), command=self.pause) # 暂停按钮
        self.pauseBut.place(x=335, y=450)
        self.startBut = Button(self.win, text="开始", height=1, width=12, font=(10), command=self.startgame)#开始按钮
        self.startBut.place(x=335, y=483)
        self.restartBut = Button(self.win, text="重新开始", height=1, width=12, font=(10), command=self.restart)#重新开始
        self.restartBut.place(x=335, y=516)
        self.quitBut = Button(self.win, text="退出", height=1, width=12, font=(10), command=self.win.quit) #self.quitgame)#退出
        self.quitBut.place(x=335, y=549)
        self.lab_score = Label(self.win, text="分数：0", font=(24))#分数
        self.lab_score.place(x=335, y=50)
        self.lab_grade = Label(self.win, text="等级：1", fg='red', font=(24))#等级
        self.lab_grade.place(x=335, y=70)
        self.check_box1 = Checkbutton(self.win, text="难度", variable=self.nandu_stat, height=1, width=3)#难度
# 菜单
        self.initgame()
        self.menu = Menu(self.win)
        self.win.config(menu=self.menu)# 创建一个下拉菜单“游戏”，包含开始和重新开始，然后将它添加到顶级菜单中
        self.startMenu = Menu(self.menu)
        self.menu.add_cascade(label='游戏', menu=self.startMenu)
        self.startMenu.add_command(label='开始', command=self.startgame)
        self.startMenu.add_separator()
        self.startMenu.add_command(label='重新开始', command=self.restart)
        self.exitMenu = Menu(self.menu)
        self.menu.add_cascade(label='退出', command=self.quitgame) # 创建一个下拉菜单“退出”，然后将它添加到顶级菜单中
        self.setMenu = Menu(self.win)
        self.menu.add_cascade(label='设置', menu=self.setMenu)   # 创建一个下拉菜单“设置”，然后将它添加到顶级菜单中
        self.setMenu.add_command(label='颜色', command=self.set_color)

#按键交互
        self.huabu.bind_all('<KeyPress-a>', self.move_left) #按a左移
        self.huabu.bind_all('<KeyPress-d>', self.move_right)#按b右移
        self.huabu.bind_all('<KeyPress-j>', self.rotate)#按j旋转
        self.huabu.bind_all('<KeyPress-s>', self.quick_drop)#s加速下移
        self.huabu.bind_all('<Left>', self.move_left)#按Left左移
        self.huabu.bind_all('<Right>', self.move_right)#按Right右移
        self.huabu.bind_all('<Up>', self.rotate)#按Up旋转
        self.huabu.bind_all('<Down>', self.quick_drop)#按Down加速下移
        self.huabu.bind_all('<KeyPress-space>', self.down_straight)#按space径直下落
        self.huabu.place(x=2, y=2) #画布的位置
        self.huabu_right.place(x=335, y=200)#下一个方块预览画布
        self.check_box1.place(x=335,y=100)
        self.fangkuai_map = [[fangk(self.huabu, i, j) for i in range(COLUMN)] for j in range(ROW)]#在这段代码中，因为y轴正方向与行数增加顺序是相反的，行数所对应的y值为582 - (ROW - self.row - 1) * (BIANCHANG + 1) ，
                                                                                                  #之后，我们在elsfk类中遍历整个画布，就能画出所有方块，只需要一行代码：
        self.win.mainloop()

#难度
    def set_nandu(self):
        self.nandu_stat = not self.nandu_stat#刚开始没有难度

    def nandu(self):
        if self.nandu_line > 10:#如果难度大于10
            self.nandu_line = 0#难度回到0
            self.base_map.pop(0)
            self.base_map.append([0] + [1] * 15) #基础地图 
            self.color_map.pop(0)
            self.color_map.append([random.randrange(0, 17) for i in range(16)])#生成随机颜色
            self.combind()
            self.draw_map()
            self.win.update()#更新窗口

    def set_color(self):
        self.muti_color = not self.muti_color



#游戏开始前的初始化
    def initgame(self):
        self.map = [[0] * COLUMN for _ in range(ROW)]  #初始化画布
        self.map_before = [[0] * COLUMN for _ in range(ROW)]
        self.base_map = [[0] * COLUMN for _ in range(ROW)]
        self.color_map = [[0] * COLUMN for _ in range(ROW)]
        self.score = 0#分数
        self.lock_operation = False#锁，类似于生产者消费者问题中的锁
        self.speed = 20#self.speed = 20 #速度
        self.last_row = 0#上次消除的行数
        self.sum_row = 0 #总共消除的行数
        self.grade = 1#等级
        self.interval = 0#下降间隔
        self.nandu_line = 0#难度行
        self.next_fangk_type = random.randrange(0, 19)#下一个方块类型
        self.next_color = random.randrange(0, 17) #下一个方块的颜色
        self.lab_score.config(text="分数：0")
        self.lab_grade.config(text="等级：1")
        self.muti_color = True  # 设置是否启用多色彩，还未弄
            
#计算分数
    def cal_score(self, row): #row -->此次消除的行数
        self.score = self.score + [row * 10, int(row * 10 * (1 + row / 10))][self.last_row == row]#这次消除行数比上次的多即可得到加成 [a,b][c]-->c成立选b，c不成立选a
        self.lab_score.config(text="分数：" + str(self.score))
        self.last_row = row
        self.sum_row += row
        self.grade = self.sum_row // 50 + 1 #分数每升高50增加一级
        self.lab_grade.config(text="等级：" + str(self.grade))
        if self.nandu_stat:
            self.nandu_line += row
            self.nandu()
            
#显示下一个方块
    def next_fk(self): #'''显示下一个方块'''
        self.cur_color = self.next_color
        self.cur_fk_type = self.next_fangk_type
        self.next_color = random.randrange(0, 17)#下一个方块的颜色
        self.next_fangk_type = random.randrange(0, 19)#下一个方块类型
        for i in self.huabu_right.find_all(): #清空上次显示画布
            self.huabu_right.delete(i)
        for i in range(4):
            fangk(self.huabu_right, 2 + self.fk_type[self.next_fangk_type][0][i], #列
                  2 - self.fk_type[self.next_fangk_type][1][i]).set_color(COLOR[self.next_color]).setvisible(1) #       位置  颜色  进行显示 
            #y轴正方向与行数增加方向相反
        self.cur_fk = self.fk_type[self.cur_fk_type]
        self.cur_location = [{'x': 7, 'y': 1}, {'x': 7, 'y': 0}][self.cur_fk_type in (2, 11, 17)]#根据当前物块类型选择初始坐标, x对应列数，y对应行数
        self.combind()
        self.draw_map()
        if not self.test_map():
            messagebox.showinfo("失败", "游戏失败了")#返回yes或no
            self.lock_operation = True


#联合
    def combind(self): #'''组合，坐标与行列之间的映射，确定显示方块的位置与颜色 '''
        self.map = [a[:] for a in self.base_map]
        for i in range(len(self.cur_fk[1])):#坐标和行列之间的映射
            x = self.cur_location['x'] + self.cur_fk[0][i]
            y = self.cur_location['y'] - self.cur_fk[1][i]
            self.map[y][x] = 1 #y高度对应行数，x对应列数，map画布就是起到决定那些位置显示方块
            self.color_map[y][x] = self.cur_color #对应位置设置当前颜色

#画出方块组合(俄罗斯方块)
    def draw_map(self):#'''画出刚出来的俄罗斯方块'''
        for i in range(ROW):
            for j in range(COLUMN):
                if self.map[i][j] != self.map_before[i][j]:
                    self.fangkuai_map[i][j].set_color(COLOR[self.color_map[i][j]]).setvisible(self.map[i][j])#把所有方块画布上的方块全设成一个颜色，但是只有map画布上为1的才显示
        self.map_before = [i[:] for i in self.map]#保存当前的显示情况
        self.win.update()#窗口更新

#下降
    def drop(self):#'''物块下降'''
        self.cur_location['y'] += 1#纵坐标增大
        if self.cur_location['y'] - min(self.cur_fk[1]) < ROW and self.test_map():#没有顶部并且可以下落
            self.combind()
            self.draw_map()
            return True
        else:
            self.cur_location['y'] -= 1 #判断不能下降后，纵坐标-1
            self.base_map = [i[:] for i in self.map]
            self.delete_row()#判断是否可以消行
            self.draw_map()
            self.next_fk()
            return False


#可移动判断
    def test_map(self):#'''可移动判断'''
        for i in range(len(self.cur_fk[0])):
            x = self.cur_location['x'] + self.cur_fk[0][i]
            y = self.cur_location['y'] - self.cur_fk[1][i]#这里self.cur_location['y']，self.cur_location['x'] 会提前加减(为了判断)
            if self.base_map[y][x] > 0: return False#   >0说明此位置有物块，不可移动
        return True


#消行
    def delete_row(self): #'''删行'''
        del_row = []
        for i in range(max(self.cur_fk[1]) - min(self.cur_fk[1]) + 1):#求遍历的行数
            if self.base_map[self.cur_location['y'] - min(self.cur_fk[1]) - i] == [1] * COLUMN:#判断所一物块下落完后的行是否全为1
                del_row.append(self.cur_location['y'] - min(self.cur_fk[1]) - i)#存储要删除的行(第几行)
        if not del_row == []:                                                   #del_row不为空说明有行要删除
            self.flash(del_row)#闪烁要删的行
            self.base_map = [r for r in self.base_map if not r == [1] * COLUMN]#把不是全1的行抽出来(相当于删行)
            self.base_map = ([[0] * COLUMN] * (30 - len(self.base_map))) + self.base_map#填0行 #每消一行，相当于顶部多一行全0， 所以必须是[0,0,0,...0] + self.base_map
            self.cal_score(len(del_row)) #计算分数


#闪烁
    def flash(self, del_rows):# '''闪烁消除的行'''
        self.lock_operation = True
        for times in range(6):#闪烁次数
            for j in del_rows:
                for i in self.fangkuai_map[j]: #fangkuai_map[j] ---> 取出第j行
                    i.setvisible(int(0.5 + times % 2 * 0.5))#闪烁效果, times为偶数，int(0)=0，times为奇数，int(1)=1
            self.win.update()
            time.sleep(0.2)#设置闪烁间隔(其实就是刷新间隔)
        self.lock_operation = False

#旋转
    def rotate(self, event):# '''旋转'''
        if not self.lock_operation:
            if self.cur_fk_type != 0:
                temp = self.cur_fk_type
                self.cur_fk_type = [(self.cur_fk_type - 7) // 4 * 4 + self.cur_fk_type % 4 + 7,
                                    (self.cur_fk_type - 1) // 2 * 2 + self.cur_fk_type % 2 + 1][
                    self.cur_fk_type in range(1, 7)]
                 #长条(1,2)、Z(3,4)、S型(5,6)方块变换都只有一种，变换的公式为
                # 变换后的类型序号 = (当前序号-1)//2 * 2 + 当前序号 % 2 + 1 
                # 1-->2, 2-->1; 3-->4, 4-->3; 5-->6, 6-->5
                #L, J, T型的变换公式：变换后的类型序号 = (当前序号-7)//4 * 4 + 当前序号 % 4 + 7
                # T型:10-->9-->8-->7-->10
                self.cur_fk = self.fk_type[self.cur_fk_type]
                if self.cur_location['x'] + min(self.cur_fk[0]) + 1 <= 0 or self.cur_location['x'] + max(
                        self.cur_fk[0]) >= COLUMN or not self.test_map() or self.cur_location['y'] + min(
                    self.cur_fk[1]) + 1 < 0: #看旋转后是否出界，出界则不旋转
                    print('testmap')
                    self.cur_fk_type = temp #还原
                    self.cur_fk = self.fk_type[self.cur_fk_type]
                     #四种情况不能旋转：
                # 旋转后会出左边界 ---> self.cur_location['x'] + min(self.cur_fk[0]) + 1 <= 0 
                # 旋转后会出右边界 ---> self.cur_location['x'] + max(self.cur_fk[0]) >= COLUMN
                # 直接旋转会和已有的物块重合 ---> self.test_map()
                # 旋转后会出上边界 ---> self.cur_location['y'] + min(self.cur_fk[1]) + 1 < 0
                self.combind()
                self.draw_map()


#加速
    def quick_drop(self, event):
        if not self.lock_operation: self.drop()#没有上锁，可按键


#左右移动
    def move_left(self, event):#左移
        if not self.lock_operation:
            self.cur_location['x'] -= 1
            if self.cur_location['x'] + min(self.cur_fk[0]) + 1 > 0 and self.test_map(): #判断是否可以左移，
                self.combind()
                self.draw_map()
            else:
                self.cur_location['x'] += 1#以及左移后是否出了左边界

    def move_right(self, event):#右移
        if not self.lock_operation:
            self.cur_location['x'] += 1
            if self.cur_location['x'] + max(self.cur_fk[0]) < COLUMN and self.test_map():#判断是否可以右移，
                self.combind()
                self.draw_map()
            else:
                self.cur_location['x'] -= 1#以及右移后是否出了右边界


                
#直接下落
    def down_straight(self, event):
        while not self.lock_operation and self.drop(): pass
        #利用循环让它自动下落，因为循环时间极短，所以人眼看的就有直接到底的感觉
   
#按钮功能

    #暂停
    def pause(self):
        messagebox.showinfo("暂停", "游戏暂停中")

    #重新开始
    def restart(self):
        messagebox.askquestion("重新开始", "确定要重新开始游戏吗？")
        for i in self.huabu.find_all():
            self.huabu.delete(i)
        self.initgame()#重新开始后需要初始
        self.startgame()#初始完毕后开始游戏

     #退出   
    def quitgame(self):
        q = messagebox.askquestion("退出", "确定要退出吗？")
        if q == 'yes': self.win.destroy(); exit()#用quit()方法开始后退不出去

     #开始游戏
    def startgame(self):
        self.check_box1.config(state=DISABLED) 
        self.startBut.config(state=DISABLED) #点击完开始按钮后不可再点击
        self.next_fk()#下一俄罗斯方块 
        while not self.lock_operation:
            time.sleep(0.05)
            if self.interval == 0: self.drop()
            self.interval = (self.interval + 1) % (22 - self.grade * 2)#每隔一段时间自动掉落
            self.win.update()  #刷新窗口界面
elsfk()
