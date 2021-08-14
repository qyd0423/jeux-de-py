from sudoku import*
from button import*
from graphics import*
class SudokuGame:
    def __init__(self,win,Pstart,length):
        self.length=length
        self.Pstart=Pstart
        self.win=win
        self.__start(win)
    def __start(self,win):
        Image_back1=Image(Point(500,500),"image\groud1.gif")
        Image_back1.draw(win)
        Button_play=Button(win,Point(500,150),100,100,"")
        Button_play.activate()
        Button_exit=Button(win,Point(800,150),100,100,"")
        Button_exit.activate()
        Button_how=Button(win,Point(200,150),150,100,"How to Play")
        Button_how.activate()
        Image_play=Image(Point(500,150),"image\play.gif")
        Image_play.draw(win)
        Image_exit=Image(Point(800,150),"image\exit.gif")
        Image_exit.draw(win)
        Image_screen=Image(Point(500,500),"image\sudoku.gif")
        Image_screen.draw(win)
        Image_welcome=Image(Point(500,900),"image\welcome.gif")
        Image_welcome.draw(win)
        while 1:
            p=win.getMouse()
            if Button_how.clicked(p):
                win.close()
                win2=GraphWin("How to Play It",800,800)
                win2.setCoords(0,0,1000,1000)
                self.__howtoplay(win2)
                break
            elif Button_play.clicked(p):
                win.close()
                win2=GraphWin("Choose the Level",800,800)
                win2.setCoords(0,0,1000,1000)
                self.__chooselevel(win2)
                break
            elif Button_exit.clicked(p):
                win.close()
                break
    def __howtoplay(self,win):
        Image_back2=Image(Point(500,500),"image\groud2.gif")
        Image_back2.draw(win)
        Image_pic=Image(Point(200,500),"image\pic.gif")
        Image_pic.draw(win)
        Image_pic=Image(Point(700,500),"image\how.gif")
        Image_pic.draw(win)
        Button_return=Button(win,Point(300,100),150,80,"Return")
        Button_return.activate()
        while 1:
            p=win.getMouse()
            if Button_return.clicked(p):
                win.close()
                win=GraphWin("",800,800)
                win.setCoords(0,0,1000,1000)
                self.__start(win)
                break
    def __chooselevel(self,win):
        Image_back3=Image(Point(500,500),"image\groud3.gif")
        Image_back3.draw(win)
        length=300
        width=100
        Button_level=[]
        Button_level.append(Button(win,Point(300,700),length,width,"EASY"))
        Image_easy=Image(Point(700,700),"image\easy.gif")
        Image_easy.draw(win)
        Button_level.append(Button(win,Point(300,500),length,width,"MEDIUM"))
        Image_medium=Image(Point(700,500),"image\medium.gif")
        Image_medium.draw(win)
        Button_level.append(Button(win,Point(300,300),length,width,"HARD"))
        Image_hard=Image(Point(700,300),"image\hard.gif")
        Image_hard.draw(win)
        Button_return=Button(win,Point(700,100),200,100,"Return")
        Button_return.activate()
        for i in range(3):
            Button_level[i].activate()
        while 1:
            p=win.getMouse()
            for i in range(3):
                if Button_level[i].clicked(p):
                    win.close()
                    win=GraphWin("Play",800,800)
                    win.setCoords(0,0,1000,1000)
                    self.__playgame(win,i+1)
                    break
            if Button_return.clicked(p):
                win.close()
                win=GraphWin("",800,800)
                win.setCoords(0,0,1000,1000)
                self.__start(win)
                break
    def __playgame(self,win,level):
        Image_back4=Image(Point(500,500),"image\groud4.gif")
        Image_back4.draw(win)
        sdk=Sudoku()
        self.sdkquestion=sdk.CreateSudoku()
        self.sdkanswer=sdk.Hideblanks(level)
        self.buttons=[]
        self.tests=[]
        self.win=win
        xstart,ystart=self.Pstart.x-self.length/2,self.Pstart.y-self.length/2
        dx=self.length*3
        for i in range(9):
            buttmp=[]
            testtmp=[]
            for j in range(9):
                tmptests=Text(Point(self.Pstart.x+j*self.length,self.Pstart.y+(8-i)*self.length),str(self.sdkquestion[i][j]))
                tmptests.setFace("courier")
                tmptests.setStyle("bold")
                tmptests.setSize(16)
                if self.sdkanswer[i][j]==0:
                    color='white'
                    tmptests.setText("")
                else :
                    color='yellow'
                tmpbuttons=Button(win,Point(self.Pstart.x+j*self.length,self.Pstart.y+(8-i)*self.length),self.length,self.length,"",color)
                tmptests.draw(win)
                buttmp.append(tmpbuttons)
                testtmp.append(tmptests)
            self.buttons.append(buttmp)
            self.tests.append(testtmp)
        for i in range(4):
            self.drawlinex(Point(xstart,ystart+dx*i),Point(xstart+dx*3,ystart+dx*i),self.win)
            self.drawliney(Point(xstart+dx*i,ystart),Point(xstart+dx*i,ystart+dx*3),self.win)
        self.Button_check=Button(win,Point(200,150),100,50,"CHECK")
        self.Button_check.activate()
        self.Button_exit=Button(win,Point(600,150),100,50,"EXIT")
        self.Button_exit.activate()
        self.Button_return=Button(win,Point(800,150),100,50,"RETURN")
        self.Button_return.activate()
        self.Button_answer=Button(win,Point(400,150),100,50,"ANSWER")
        self.Button_answer.activate()
        self.numbuttons=[]
        for i in range(10):
            tmpbuttons=Button(win,Point(230+i*60,300),60,60,str(i))
            tmpbuttons.activate()
            self.numbuttons.append(tmpbuttons)
        self.getButton()
    def drawlinex(self,p1,p2,win):
        sy=p1.y-1.5
        while sy<=p1.y+1.5:
            l=Line(Point(p1.x,sy),Point(p2.x,sy))
            l.draw(win)
            sy+=.1
    def drawliney(self,p1,p2,win):
        sx=p1.x-1.5
        while sx<=p1.x+1.5:
            l=Line(Point(sx,p1.y),Point(sx,p2.y))
            l.draw(win)
            sx+=.1
    def getButton(self):
        while 1:
            p=self.win.getMouse()
            x,y=p.getX(),p.getY()
            for i in range(9):
                for j in range(9):
                    b=self.buttons[i][j]
                    if b.xmin <= x <= b.xmax and\
                       b.ymin <= y <= b.ymax and\
                       self.sdkanswer[i][j]==0:
                        for i in range(9):
                            for j in range(9):
                                self.buttons[i][j].deactivate()
                        b.activate()                        
            for b in self.numbuttons:
                if b.clicked(p) and self.sthactived():
                    c=b.getLabel()
                    d=int(c)
                    if d==0:
                        c=""
                    for i in range(9):
                        for j in range(9):
                            if self.buttons[i][j].active==1:
                                self.tests[i][j].setText(c)
            if self.Button_check.clicked(p):
                self.checkanswer()
            if self.Button_exit.clicked(p):
                self.win.close()
                break
            if self.Button_return.clicked(p):
                self.win.close()
                win2=GraphWin("Choose the Level",800,800)
                win2.setCoords(0,0,1000,1000)
                self.__chooselevel(win2)
                break
            if self.Button_answer.clicked(p):
                for i in range(9):
                    for j in range(9):
                        c=str(self.sdkquestion[i][j])
                        self.tests[i][j].setText(c)
    def sthactived(self):
        for i in range(9):
            for j in range(9):
                if self.buttons[i][j].active==1:
                    return 1
        return 0
    def checkanswer(self):
        youranswer=[]
        win3=GraphWin("Wait",400,200)
        Image_back5=Image(Point(200,100),"image\groud5.gif")
        Image_back5.draw(win3)
        checktest=Text(Point(200,100),"Wait")
        checktest.draw(win3)
        for i in range(9):
            tmp=[]
            for j in range(9):
                a=self.tests[i][j].getText()
                if a=='':
                    d=0
                else :
                    d=int(a)
                tmp.append(d)
            youranswer.append(tmp)
        checklist=[0,0,0,0,0,0,0,0,0]
        flag=1
        for i in range(9):
            for j in range(9):
                checklist[j]=youranswer[i][j]
            if self.checkit(checklist):
                flag=0  
        for i in range(9):
            for j in range(9):
                checklist[j]=youranswer[j][i]
            if self.checkit(checklist):
                flag=0
        for i in range(3):
            for j in range(3):
                for k in range(3*i,3*i+3,1):
                    for l in range(3*j,3*j+3,1):
                        tmp=(3*k+l)%9
                        checklist[tmp]=youranswer[k][l]
                if self.checkit(checklist):
                    flag=0
        if flag==0:
            checktest.setText("You got a wrong answer!")
            Image_lose=Image(Point(350,100),"image\lose.gif")
            Image_lose.draw(win3)
            Button_back=Button(win3,Point(100,150),60,30,"Back")
            Button_back.activate()
            while 1:
                p=win3.getMouse()
                if Button_back.clicked(p):
                    win3.close()
                    break
        else :
            checktest.setText("You got it!")
            Image_win=Image(Point(350,100),"image\win.gif")
            Image_win.draw(win3)
            Button_retry=Button(win3,Point(100,150),60,30,"Retry")
            Button_retry.activate()
            while 1:
                p=win3.getMouse()
                if Button_retry.clicked(p):
                    win3.close()
                    self.win.close()
                    win2=GraphWin("Choose the Level",800,800)
                    win2.setCoords(0,0,1000,1000)
                    self.__chooselevel(win2)
    def checkit(self,ar):
        for i in range(9):
            for j in range(i):
                if ar[j]==ar[i] or ar[i]==0:
                    return 1
        return 0
    
if __name__=='__main__':
    win=GraphWin("Sudoku game",800,800)
    win.setCoords(0,0,1000,1000)
    a=SudokuGame(win,Point(300,400),50.0)
    
                







        
        
