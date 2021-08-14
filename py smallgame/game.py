import random
import gofish
from tkinter import *
from tkinter import messagebox  # 此方法不在ALL中  需要导入
import turtle
import time
import os
from Bugbits import snake_eat_beans_v1 as snake_eat
import Tetris


def guess_num():
    rang1 = int(input("please enter the minimum for the range what you wanna guess ! \n>>>"))
    rang2 = int(input("please enter the maximum for the range what you wanna guess ! \n>>>"))
    num = random.randint(rang1, rang2)
    guess = "guess"
    i = 0

    while guess != num:
        i += 1
        guess = int(input("Please enter the number what you guess ! \n>>>"))
        if guess == num:
            print("Congratulation！ You Got it!!! ")
        elif guess < num:
            print("Your guess is too small! ")
        else:
            print("Your guess is too large! ")

    print(f"You have guessed {i} times")


# 1-2画心形圆弧
def hart_arc():
    for i in range(200):
        turtle.right(1)
        turtle.forward(2)


def move_pen_position(x, y):
    turtle.hideturtle()  # 隐藏画笔（先）
    turtle.up()  # 提笔
    turtle.goto(x, y)  # 移动画笔到指定起始坐标（窗口中心为0,0）
    turtle.down()  # 下笔
    turtle.showturtle()  # 显示画笔


def drawlove():
    love = 'Estelle && Quentin'
    # signature = 'Estelle & Quentin'
    # date = 'You potato me '

    # 1-3初始化
    turtle.setup(width=800, height=500)  # 窗口（画布）大小
    turtle.color('red', 'pink')  # 画笔颜色
    turtle.pensize(3)  # 画笔粗细
    turtle.speed(5)  # 描绘速度
    # 初始化画笔起始坐标
    move_pen_position(x=0, y=-180)  # 移动画笔位置
    turtle.left(140)  # 向左旋转140度

    turtle.begin_fill()  # 标记背景填充位置

    # 1-4画图和展示
    turtle.forward(224)  # 向前移动画笔，长度为224
    # 画爱心圆弧
    hart_arc()  # 左侧圆弧
    turtle.left(120)  # 调整画笔角度
    hart_arc()  # 右侧圆弧
    # 画心形直线（ 右下方 ）
    turtle.forward(224)

    turtle.end_fill()  # 标记背景填充结束位置

    move_pen_position(x=70, y=160)  # 移动画笔位置
    turtle.left(185)  # 向左旋转180度
    turtle.circle(-110, 185)  # 右侧圆弧
    # 画心形直线（ 右下方 ）
    # turtle.left(20)  # 向左旋转180度
    turtle.forward(50)
    move_pen_position(x=-180, y=-180)  # 移动画笔位置
    turtle.left(180)  # 向左旋转140度

    # 画心形直线（ 左下方 ）
    turtle.forward(600)  # 向前移动画笔，长度为224

    # 在心形中写上表白话语
    move_pen_position(0, 50)  # 表白语位置
    turtle.hideturtle()  # 隐藏画笔
    turtle.color('#CD5C5C', 'pink')  # 字体颜色
    # font:设定字体、尺寸（电脑下存在的字体都可设置）  align:中心对齐
    turtle.write(love, font=('Arial', 20, 'bold'), align="center")

    # 签写署名和日期
    turtle.color('red', 'pink')
    time.sleep(2)
    # move_pen_position(220, -180)
    # turtle.hideturtle()  # 隐藏画笔
    # turtle.write(signature, font=('Arial', 20), align="center")
    # move_pen_position(220, -220)
    # turtle.hideturtle()  # 隐藏画笔
    # turtle.write(date, font=('Arial', 20), align="center")

    # 1-5点击窗口关闭程序
    window = turtle.Screen()
    window.exitonclick()


# 点击关闭弹出提示消息
def closeWindow():  # 不允许关闭窗口
    messagebox.showinfo(title='警告', message='不许关闭，好好回答')
    return


# 点击喜欢的确定  关闭所有窗口
def closeallwindow():
    window.destroy()


# 点击喜欢弹出窗口
def Love():
    # 是一个独立的顶级窗口，
    love = Toplevel(window)
    love.geometry('300x200+520+260')
    love.title('答应我')
    label = Label(love, text='好的,老婆', font=('宋体', 30), fg='red')
    label.pack()
    btn = Button(love, text='老公，你再说一遍我录个音', width=20, height=2, command=closeallwindow)
    btn.pack()
    love.protocol('WM_DELETE_WINDOW', closelove)
    drawlove()


# 点击喜欢关闭
def closelove():
    messagebox.showinfo('不再考虑一下吗', message='在考虑一下吧')
    return


def closenolove():
    nolove()


# 点击不喜欢的方法
def nolove():
    nolove = Toplevel(window)
    nolove.geometry('300x100+520+260')
    nolove.title('重选')
    label = Label(nolove, text='那你是想娶我？重新选', font=('楷体', 15))
    label.pack()
    btn = Button(nolove, text='好，重新选', width=10, height=2, command=nolove.destroy)
    btn.pack()
    nolove.protocol('WM_DELETE_WINDOW', closenolove)


def start_game():
    tempt = ">>>"
    print("==========================")
    index = input(f'''1:Devinez le nombre
2:le go-fish 
3:Tetris
4:Bug Bits
0:exit
输入其他数字有彩蛋哦
{tempt}''')
    if index == '1':
        guess_num()
    elif index == '2':
        gofish.play()
    elif index == '3':
        Tetris.elsfk()
    elif index == '4':
        snake_eat.play()
    elif index == '0':
        exit()
    elif index == '520' or index == '423' or index == '523':
            # 创建窗口
            window = Tk()
            # 设置窗口标题
            window.title('嫁给我好吗')
            # 设置窗口大小
            window.geometry('380x150+520+213')

            window.protocol('WM_DELETE_WINDOW', closeWindow)

            # 标签控件
            label1 = Label(window, text='韩淼', font=('微软雅黑', 15), fg='red')
            # 定位    grid   网格式布局     pack       很少用-place
            label1.grid()

            label2 = Label(window, text='嫁给我好吗？', font=('黑体', 27))
            # sticky  对齐方法   N  S  W  E
            label2.grid(row=1, column=1, sticky=E)

            # 按钮
            btn1 = Button(window, text='好', width=15, height=2, command=Love)
            btn1.grid(row=3, column=0, sticky=W)

            btn2 = Button(window, text='不好', width=15, height=2, command=nolove)
            btn2.grid(row=3, column=1, sticky=E)

            # 显示窗口    消息循环
            window.mainloop()
    else:
        print("ERROR: The order what you entered is not correct,please enter it again")



if __name__ == "__main__":
    while True:
        start_game()
