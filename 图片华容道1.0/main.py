#coding:utf-8
import copy
import sys
import random
from PyQt5 import QtGui
import requestion
from enum import IntEnum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox, QMainWindow, QPushButton

# 棋盘的类，实现移动和扩展状态
target = []
ans = ""
step = 0
swap = []
uuid = ""
zuhao = 0
listproblem = []
disnumber = 0
myswap = [0, 0]
operations = ""


class grid:
    def __init__(self, stat):
        self.pre = None
        # 目标状态
        # stat是一个二维列表
        self.stat = stat
        self.find0()
        self.update()

    # 更新启发函数的相关信息
    def update(self):
        self.fH()
        self.fG()
        self.fF()

    # G是深度，也就是走的步数
    def fG(self):
        if self.pre is not None:
            self.G = self.pre.G + 1
        else:
            self.G = 0

    # H是和目标状态距离之和
    def fH(self):
        self.H = 0
        for i in range(3):
            for j in range(3):
                targetX = target[i][j]
                nowP = self.findx(targetX)
                # 曼哈顿距离之和
                self.H += abs(nowP[0] - i) + abs(nowP[1] - j)

    # F是启发函数，F=G+H
    def fF(self):
        self.F = self.G + self.H

    # 查看找到的解是如何从头移动的
    def seeAns(self):
        global ans
        ans = ""
        p = self
        while p.pre:
            x1, y1 = p.find2()
            p = p.pre
            x2, y2 = p.find2()
            if x2 > x1:
                ans += "w"
            elif x2 < x1:
                ans += "s"
            elif x2 == x1:
                if y2 > y1:
                    ans += "a"
                elif y2 < y1:
                    ans += "d"
        listans = list(ans)
        listans.reverse()
        ans = "".join(listans)
        print(ans)

    def find2(self):
        for i in range(3):
            if 0 in self.stat[i]:
                j = self.stat[i].index(0)
                return i, j

    # 找到数字x的位置
    def findx(self, x):
        for i in range(3):
            if x in self.stat[i]:
                j = self.stat[i].index(x)
                return [i, j]

    # 找到0，也就是空白格的位置
    def find0(self):
        self.zero = self.findx(0)

    # 扩展当前状态，也就是上下左右移动。返回的是一个状态列表，也就是包含stat的列表
    def expand(self):
        i = self.zero[0]
        j = self.zero[1]
        gridList = []
        if j == 2 or j == 1:
            gridList.append(self.left())
        if i == 2 or i == 1:
            gridList.append(self.up())
        if i == 0 or i == 1:
            gridList.append(self.down())
        if j == 0 or j == 1:
            gridList.append(self.right())
        return gridList

    # deepcopy多维列表的复制，防止指针赋值将原列表改变
    # move只能移动行或列，即row和col必有一个为0
    # 向某个方向移动
    def move(self, row, col):
        newStat = copy.deepcopy(self.stat)
        tmp = self.stat[self.zero[0] + row][self.zero[1] + col]
        newStat[self.zero[0]][self.zero[1]] = tmp
        newStat[self.zero[0] + row][self.zero[1] + col] = 0
        return newStat

    def up(self):
        return self.move(-1, 0)

    def down(self):
        return self.move(1, 0)

    def left(self):
        return self.move(0, -1)

    def right(self):
        return self.move(0, 1)


# 判断状态g是否在状态集合中，g是对象，gList是对象列表
# 返回的结果是一个列表，第一个值是真假，如果是真则第二个值是g在gList中的位置索引
def isin(g, gList):
    gstat = g.stat
    statList = []
    for i in gList:
        statList.append(i.stat)
    if gstat in statList:
        res = [True, statList.index(gstat)]
    else:
        res = [False, 0]
    return res


# 计算不在位的个数
def getcost(alist):
    cost = 0
    for row in range(3):
        for column in range(3):
            if alist[row][column] == 0:
                pass
                # 值是否对应
            elif alist[row][column] != row * 3 + column + 1:
                cost = cost + 1
    return cost


# 计算逆序数之和
def N(nums):
    count = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            for j in range(i):
                if nums[j] > nums[i]:
                    count += 1
    return count


# 根据逆序数之和判断所给八数码是否可解
def judge(src, target1):
    src = src[0] + src[1] + src[2]
    target1 = target1[0] + target1[1] + target1[2]
    N1 = N(src)
    N2 = N(target1)
    if N1 % 2 == N2 % 2:
        return True
    else:
        return False


# Astar算法的函数
def Astar(startStat):
    # open和closed存的是grid对象
    openlist = []
    closed = []
    # 初始化状态
    g = grid(startStat)
    # 检查是否有解
    if not judge(startStat, target):
        print("无解")
        exit(1)

    openlist.append(g)
    # time变量用于记录遍历次数
    time = 0
    # 当open表非空时进行遍历
    while openlist:
        # 根据启发函数值对open进行排序，默认升序
        openlist.sort(key=lambda G: G.F)
        # 找出启发函数值最小的进行扩展
        minFStat = openlist[0]
        # 检查是否找到解，如果找到则从头输出移动步骤
        if minFStat.H == 0:
            print("found and times:", time, "moves:", minFStat.G)
            minFStat.seeAns()
            break

        # 走到这里证明还没有找到解，对启发函数值最小的进行扩展
        openlist.pop(0)
        closed.append(minFStat)
        expandStats = minFStat.expand()
        # 遍历扩展出来的状态
        for stat in expandStats:
            # 将扩展出来的状态（二维列表）实例化为grid对象
            tmpG = grid(stat)
            # 指针指向父节点
            tmpG.pre = minFStat
            # 初始化时没有pre，所以G初始化时都是0
            # 在设置pre之后应该更新G和F
            tmpG.update()
            # 查看扩展出的状态是否已经存在与open或closed中
            findstat = isin(tmpG, openlist)
            findstat2 = isin(tmpG, closed)
            # 在closed中,判断是否更新
            if findstat2[0] == True and tmpG.F < closed[findstat2[1]].F:
                closed[findstat2[1]] = tmpG
                openlist.append(tmpG)
                time += 1
            # 在open中，判断是否更新
            if findstat[0] == True and tmpG.F < openlist[findstat[1]].F:
                openlist[findstat[1]] = tmpG
                time += 1
            # tmpG状态不在open中，也不在closed中
            if findstat[0] == False and findstat2[0] == False:
                openlist.append(tmpG)
                time += 1


# 用枚举类表示方向
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# 设置参数
def set(x, y, z, p, q, r):
    global step
    global swap
    global uuid
    global zuhao
    global listproblem
    global disnumber
    step = x
    swap = y.copy()
    uuid = z
    zuhao = p
    listproblem = q
    disnumber = r


class NumberHuaRong(QWidget):
    """ 华容道主体 """

    def __init__(self):
        super().__init__()
        self.numbers = list(range(1, 10))
        self.blocks = []
        # 0的坐标
        self.zero_row = 0
        self.zero_column = 0
        self.disnum = 0  # 缺的数字位置
        self.gltMain = QGridLayout()
        self.cost = 0
        self.mylist = []
        self.goal = []
        self.initUI()
        self.ans = ""
        self.count = 0

    def initUI(self):
        # 设置方块间隔
        self.gltMain.setSpacing(10)

        self.onInit()

        # 设置布局
        self.setLayout(self.gltMain)
        # 设置宽和高
        self.setFixedSize(950, 950)
        # 设置标题和图标
        self.setWindowTitle('图片华容道              WASD：移动白块   R:返回   Z：解题   C:演示')
        self.setWindowIcon(QIcon("图标.png"))
        # 设置背景颜色
        self.setStyleSheet("background-color:gray;")
        self.show()

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        global ans
        ans = ""
        self.ans = ""
        self.count = 0
        self.disnum = disnumber  # 缺的数字
        self.numbers = list(range(1, 10))
        self.numbers[self.disnum - 1] = 0
        # 将数字添加到二维数组
        self.blocks = copy.deepcopy(listproblem)
        for row in range(3):
            for column in range(3):
                temp = self.blocks[row][column]
                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
        # 打乱数组
        '''for i in range(5000):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))'''
        self.mylist = self.blocks.copy()
        self.updatePanel()
        # self.solve3()

    # 检测按键
    def keyPressEvent(self, event):
        global ans
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            self.move(Direction.DOWN)
        if key == Qt.Key_Down or key == Qt.Key_S:
            self.move(Direction.UP)
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.move(Direction.RIGHT)
        if key == Qt.Key_Right or key == Qt.Key_D:
            self.move(Direction.LEFT)
        if key == Qt.Key_Z:
            self.solve()
            self.ans = ans
        if key == Qt.Key_C:
            mm = self.ans[self.count]
            if mm == 'w':
                self.move(Direction.DOWN)
            elif mm == 's':
                self.move(Direction.UP)
            elif mm == 'a':
                self.move(Direction.RIGHT)
            elif mm == 'd':
                self.move(Direction.LEFT)
            self.updatePanel()
            self.count += 1

        if key == Qt.Key_R:
            self.close()
            self.f = FirstUi()
            self.f.show()
        self.updatePanel()
        if self.checkResult():
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战！'):
                self.onInit()  # 结束后重新开始


    # 方块移动算法
    def move(self, direction):
        if direction == Direction.UP:  # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if direction == Direction.DOWN:  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if direction == Direction.LEFT:  # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if direction == Direction.RIGHT:  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.gltMain.addWidget(Block(self.blocks[row][column]), row, column)
        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        for row in range(3):
            for column in range(3):
                if row == self.zero_row and column == self.zero_column:
                    pass
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

        return True

    def change(self, x):
        global myswap
        row1 = int((x[0] - 1) / 3)
        col1 = (x[0] - 1) % 3
        row2 = int((x[1] - 1) / 3)
        col2 = (x[1] - 1) % 3
        print('第{0}步 强制交换{1}：'.format(step, swap))
        # print('强制交换前', self.blocks)
        self.blocks[row1][col1], self.blocks[row2][col2] = self.blocks[row2][col2], self.blocks[row1][col1]
        # print('强制交换后',self.blocks)
        if judge(self.blocks, self.goal):
            return
        else:
            mini = 10
            flag1 = 0
            flag2 = 0
            for i in range(9):
                for j in range(i, 9):
                    list1 = copy.deepcopy(self.blocks)
                    row1 = int(i / 3)
                    col1 = i % 3
                    row2 = int(j / 3)
                    col2 = j % 3
                    list1[row1][col1], list1[row2][col2] = list1[row2][col2], list1[row1][col1]
                    if judge(list1, self.goal):
                        thiscost = getcost(list1)
                        if mini > thiscost:
                            mini = thiscost
                            flag1 = i
                            flag2 = j
            row1 = int(flag1 / 3)
            col1 = flag1 % 3
            row2 = int(flag2 / 3)
            col2 = flag2 % 3
            # print('用户交换前', self.blocks)
            self.blocks[row1][col1], self.blocks[row2][col2] = self.blocks[row2][col2], self.blocks[row1][col1]
            print('无解，进行用户交换{0}：'.format([flag1+1, flag2+1]))
            # print('用户交换后', self.blocks)
            myswap = [flag1 + 1, flag2 + 1]
            return

    def solve(self):
        self.goal = []
        for row in range(3):
            self.goal.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                self.goal[row].append(temp)
        global target
        target = self.goal.copy()
        stat = self.mylist
        global operations
        if not judge(stat, target):
            print('一开始无解，随机移动到step步再进行解题')
            anscopy = ""
            print(self.zero_row,self.zero_column)
            for i in range(step):
                if self.zero_row == 0:
                    anscopy += 's'
                    self.move(Direction.UP)
                else:
                    anscopy += 'w'
                    self.move(Direction.DOWN)
            self.change(swap)
            stat = self.mylist
            Astar(stat)
            anscopy = anscopy + ans
            operations = anscopy
        else:
            Astar(stat)
            if len(ans) <= step:
                operations = ans
            else:
                anscopy = ans[0:step]
                for i in range(step):
                    mm = ans[i]
                    if mm == 'w':
                        self.move(Direction.DOWN)
                    elif mm == 's':
                        self.move(Direction.UP)
                    elif mm == 'a':
                        self.move(Direction.RIGHT)
                    elif mm == 'd':
                        self.move(Direction.LEFT)
                self.change(swap)
                stat = self.mylist
                Astar(stat)
                anscopy = anscopy + ans
                operations = anscopy

        print('uuid=', uuid)
        print('operations=', operations)
        print('myswap=', myswap)
        requestion.submit(uuid, operations, myswap)


class NumberHuaRong2(QWidget):
    """ 华容道主体 """

    def __init__(self):
        super().__init__()
        self.numbers = list(range(1, 10))
        self.blocks = []
        # 0的坐标
        self.zero_row = 0
        self.zero_column = 0
        self.disnum = 0  # 缺的数字位置
        self.gltMain = QGridLayout()
        self.cost = 0
        self.mylist = []
        self.goal = []
        self.initUI()
        self.ans = ""
        self.count = 0

    def initUI(self):
        # 设置方块间隔
        self.gltMain.setSpacing(10)

        self.onInit()

        # 设置布局
        self.setLayout(self.gltMain)
        # 设置宽和高
        self.setFixedSize(950, 950)
        # 设置标题和图标
        self.setWindowTitle('图片华容道          WASD：移动白块   R:返回   Z：解题   C:演示')
        self.setWindowIcon(QIcon("图标.png"))
        # 设置背景颜色
        self.setStyleSheet("background-color:gray;")
        self.show()

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        self.ans = ""
        self.count = 0
        self.score = 0
        self.rand = random.randint(1, 9)  # 缺的数字
        self.numbers = list(range(1, 10))
        self.numbers[self.rand - 1] = 0
        # 将数字添加到二维数组
        self.blocks = []
        for row in range(3):
            self.blocks.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                # print(temp)
                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column

                self.blocks[row].append(temp)
        for i in range(500):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        self.mylist = self.blocks.copy()
        self.updatePanel()
    # 检测按键
    def keyPressEvent(self, event):
        global ans
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            self.move(Direction.DOWN)
            self.score += 1
        if key == Qt.Key_Down or key == Qt.Key_S:
            self.move(Direction.UP)
            self.score += 1
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.move(Direction.RIGHT)
            self.score += 1
        if key == Qt.Key_Right or key == Qt.Key_D:
            self.move(Direction.LEFT)
            self.score += 1
        if key == Qt.Key_Z:
            self.solve()
            self.ans = ans
        if key == Qt.Key_C:
            mm = self.ans[self.count]
            if mm == 'w':
                self.move(Direction.DOWN)
                self.score += 1
            elif mm == 's':
                self.move(Direction.UP)
                self.score += 1
            elif mm == 'a':
                self.move(Direction.RIGHT)
                self.score += 1
            elif mm == 'd':
                self.move(Direction.LEFT)
                self.score += 1
            self.updatePanel()
            self.count += 1

        if key == Qt.Key_R:
            self.close()
            self.f = FirstUi()
            self.f.show()
        self.updatePanel()
        if self.checkResult():
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战！\n本次挑战得分:'+str(self.score)):
                #写入得分
                with open("score.txt","a+",encoding="utf-8") as fp:
                    fp.write(str(self.score)+'\n')
                print(self.score)
                self.onInit()  # 结束后重新开始


    # 方块移动算法
    def move(self, direction):
        if direction == Direction.UP:  # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if direction == Direction.DOWN:  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if direction == Direction.LEFT:  # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if direction == Direction.RIGHT:  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.gltMain.addWidget(Block2(self.blocks[row][column]), row, column)
        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        for row in range(3):
            for column in range(3):
                if row == self.zero_row and column == self.zero_column:
                    pass
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

        return True

    def solve(self):
        self.goal = []
        for row in range(3):
            self.goal.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                self.goal[row].append(temp)
        global target
        target = self.goal.copy()
        stat = self.mylist
        global operations
        Astar(stat)


class Block(QLabel):
    """ 数字方块 """

    def __init__(self, number):
        super().__init__()
        self.imgPath = ["D://0作业/软工实践/hrd/确定序列/" + str(zuhao) + "_" + str(i) + ".jpg" for i in range(1, 10)]
        self.number = number
        self.setFixedSize(300, 300)  # 控制窗体大小
        if self.number > 0:
            # 导入图片
            imgName = self.imgPath[number - 1]
            pix = QPixmap(imgName)
            lb1 = QLabel(self)
            lb1.setPixmap(pix)

        if self.number == 0:
            self.setStyleSheet("background-color:white;border-radius:10px;")

class Block2(QLabel):
    """ 数字方块 """

    def __init__(self, number):
        super().__init__()
        self.imgPath = ["sub" + str(i) + ".png" for i in range(1, 10)]
        self.number = number
        self.setFixedSize(300, 300)  # 控制窗体大小
        if self.number > 0:
            # 导入图片
            imgName = self.imgPath[number - 1]
            pix = QPixmap(imgName)
            lb1 = QLabel(self)
            lb1.setPixmap(pix)

        if self.number == 0:
            self.setStyleSheet("background-color:white;border-radius:10px;")


class FirstUi(QMainWindow):
    def __init__(self):
        super(FirstUi, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(950, 950)
        self.setWindowTitle('图片华容道')
        self.setWindowIcon(QIcon("图标.png"))
        #设置背景
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("back.jpg").scaled(950,950)))
        self.setPalette(window_pale)

        self.label = QLabel(self)
        self.label.setGeometry(275, 100, 600, 200)
        self.label.setText("图片华容道")
        self.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:90px;font-weight:bold;font-family:楷体;}")
        self.btn1 = QPushButton('开始游戏', self)
        self.btn1.setGeometry(365, 350, 225, 75)
        self.btn1.setStyleSheet("QPushButton{color:black;font-size:40px}"
                                       "QPushButton:hover{background-color:lightgreen}"
                                       "QPushButton{background-color:lightblue}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:10px}"
                                       "QPushButton{padding:2px 4px}"
                                       )
        self.btn1.clicked.connect(self.slot_btn_function3)
        self.btn2 = QPushButton('游戏规则', self)
        self.btn2.setGeometry(365, 500,225,75)
        self.btn2.setStyleSheet("QPushButton{color:black;font-size:40px}"
                                       "QPushButton:hover{background-color:lightgreen}"
                                       "QPushButton{background-color:lightblue}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:10px}"
                                       "QPushButton{padding:2px 4px}"
                                       )
        self.btn2.clicked.connect(self.slot_btn_function2)
        self.btn3 = QPushButton('联网解题模式', self)
        self.btn3.setGeometry(365, 650, 225,75)
        self.btn3.setStyleSheet("QPushButton{color:black;font-size:35px}"
                                       "QPushButton:hover{background-color:lightgreen}"
                                       "QPushButton{background-color:lightblue}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:10px}"
                                       "QPushButton{padding:2px 4px}"
                                       )
        self.btn3.clicked.connect(self.slot_btn_function1)

        self.btn1 = QPushButton('历史得分', self)
        self.btn1.setGeometry(365, 800, 225,75)
        self.btn1.setStyleSheet("QPushButton{color:black;font-size:40px}"
                                "QPushButton:hover{background-color:lightgreen}"
                                "QPushButton{background-color:lightblue}"
                                "QPushButton{border:2px}"
                                "QPushButton{border-radius:10px}"
                                "QPushButton{padding:2px 4px}"
                                )
        self.btn1.clicked.connect(self.slot_btn_function4)

    def slot_btn_function1(self):
        self.close()
        self.s = NumberHuaRong()
        self.s.show()
    def slot_btn_function2(self):
        self.hide()
        self.s = SecondUi()
        self.s.show()
    def slot_btn_function3(self):
        self.close()
        self.s = NumberHuaRong2()
        self.s.show()
    def slot_btn_function4(self):
        self.close()
        self.s = ThirdUi()
        self.s.show()
class SecondUi(QWidget):
    def __init__(self):
        super(SecondUi, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(950, 950)
        self.setWindowTitle('游戏规则')
        self.setWindowIcon(QIcon("图标.png"))
        #设置背景
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("back.jpg").scaled(950,950)))
        self.setPalette(window_pale)

        self.label1 = QLabel(self)
        self.label1.setGeometry(350, 50, 255, 150)
        self.label1.setText("游戏规则")
        self.label1.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:60px;font-weight:bold;font-family:楷体;}")

        self.label = QLabel(self)
        self.label.setGeometry(150, 150, 600, 600)
        self.label.setText("1.将原始字符图片平均切割成九份小图，并随机抠掉一张图充当空格，此时图片为原始状态，然后我们将小图的顺序打乱并拼接回去，你需要做的事就是移动白色的图片将图片恢复到原始的状态\n\n2.当你移动到一定步数的时候，我们会强制调换此时棋盘上的两个格子，由于此时棋盘不一定有解，所以我们给了你一次自由调换的机会，你可以调换任意两个图片的位置，注意这个自由调换只能在棋盘无解的情况下使用，且需紧接着强制调换的操作。\n\n3.按Z解题，按C进行AI提示")
        self.label.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:30px;}")
        self.label.setWordWrap(True)

        self.btn = QPushButton('返回主页面', self)
        self.btn.setGeometry(0, 0, 225, 75)
        self.btn.setStyleSheet("QPushButton{color:black;font-size:40px}"
                               "QPushButton:hover{background-color:lightgreen}"
                               "QPushButton{background-color:lightblue}"
                               "QPushButton{border:2px}"
                               "QPushButton{border-radius:10px}"
                               "QPushButton{padding:2px 4px}"
                               )
        self.btn.clicked.connect(self.slot_btn_function)

    def slot_btn_function(self):
        self.hide()
        self.f = FirstUi()
        self.f.show()

class ThirdUi(QWidget):
    def __init__(self):
        super(ThirdUi, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(950, 950)
        self.setWindowTitle('历史得分')
        self.setWindowIcon(QIcon("图标.png"))
        #设置背景
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("back.jpg").scaled(950,950)))
        self.setPalette(window_pale)

        self.label1 = QLabel(self)
        self.label1.setGeometry(350, 50, 255, 150)
        self.label1.setText("历史得分")
        self.label1.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:60px;font-weight:bold;font-family:楷体;}")
        self.label = QLabel(self)
        self.label.setGeometry(400, 150, 600, 800)
        with open("score.txt","r",encoding="utf-8") as fp:
            scores = fp.readlines()
            ls = []#只保留前15个记录
            for score in scores:
                ls.append(int(score.replace('\n', '')))
            ls = sorted(ls)
            finalstr = ' 步数\n'
            if len(ls)>=15:
                for i in range(15):
                    if i<9:
                        finalstr += (str(i + 1) + '.' +"  "+ str(ls[i]) + '\n')
                    else:
                        finalstr += (str(i+1)+'.'+" " +str(ls[i])+'\n')
            else:
                for i in range(len(ls)):
                    if i<9:
                        finalstr += (str(i + 1) + '.' +"  "+ str(ls[i]) + '\n')
                    else:
                        finalstr += (str(i+1)+'.'+" " +str(ls[i])+'\n')
            self.label.setText(finalstr)
            self.label.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:40px;font-weight:bold;font-family:楷体;}")
        # self.label.setStyleSheet("QLabel{color:rgb(33,215,217,255)}")
        self.btn = QPushButton('返回主页面', self)
        self.btn.setGeometry(0, 0, 225, 75)
        self.btn.setStyleSheet("QPushButton{color:black;font-size:40px}"
                               "QPushButton:hover{background-color:lightgreen}"
                               "QPushButton{background-color:lightblue}"
                               "QPushButton{border:2px}"
                               "QPushButton{border-radius:10px}"
                               "QPushButton{padding:2px 4px}"
                               )
        self.btn.clicked.connect(self.slot_btn_function)

    def slot_btn_function(self):
        self.hide()
        self.f = FirstUi()
        self.f.show()

if __name__ == '__main__':
    step, swap, uuid, zuhao, listproblem, dis = requestion.getproblem()
    set(step, swap, uuid, zuhao, listproblem, dis)
    app = QApplication(sys.argv)
    w = FirstUi()
    w.show()
    sys.exit(app.exec_())