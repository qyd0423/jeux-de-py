from random import*
class Sudoku:
    def __init__(self):
        self.seed=[[5,2,9,4,3,7,6,8,1],[7,6,1,8,9,2,4,5,3],[3,8,4,6,1,5,2,7,9],
                   [4,7,8,3,2,6,9,1,5],[6,3,5,1,8,9,7,4,2],[9,1,2,5,7,4,3,6,8],
                   [1,4,6,2,5,3,8,9,7],[8,9,3,7,6,1,5,2,4],[2,5,7,9,4,8,1,3,6]]
        self.problem=[]
        for i in range(9):
            self.problem.append([0,0,0,0,0,0,0,0,0])
        self.randomlist=self.__randomArray()
    def __randomArray(self):
        tmplist=[]
        for i in range(9):
            ran=randrange(1,10)
            while 1:
                if not(ran in tmplist):
                    tmplist.append(ran)
                    break
                ran=randrange(1,10)
        return tmplist
    def CreateSudoku(self):
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if self.seed[i][j]==self.randomlist[k]:
                        tmp=(k+1)%9
                        self.seed[i][j]=self.randomlist[tmp]
                        break
        return self.seed
    def Hideblanks(self,level):
        for i in range(9):
            for j in range(9):
                if random()<float(level+1)/6:
                    self.problem[i][j]=0
                else :
                    self.problem[i][j]=self.seed[i][j]
        return self.problem
    def printSudoku(self):
        for i in range(9):
            print(self.problem[i])
        for i in range(9):
            print(self.seed[i])
