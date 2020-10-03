# 把数字改为图片

import random
import sys
import copy
from enum import IntEnum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox

g_ListArr = []  # 当前的待识别队列
g_readArr = []  # 已读状态队列


class StruNum:
    myList = []
    myPreList = []
    myCost = 0

    def __init__(self, itlist=None, prelist=None, cost=0, goallist=None):
        if goallist is None:
            goallist = []
        if prelist is None:
            prelist = []
        if itlist is None:
            itlist = []
        self.myList = itlist
        self.myPreList = prelist
        self.myCost = cost
        self.goal = goallist.copy()

    def SetPre(self, newPreList):
        self.myPreList = newPreList
        self.myCost = newPreList.mycost

    def IsSame(self, struNum1):
        if self.myList == struNum1.myList:
            return True
        else:
            return False

    def GetItsPre(self):
        global g_readArr
        for i in range(0, len(g_readArr), 1):
            if self.myPreList == g_readArr[i].myList:
                return g_readArr[i]

    def GetZeroIndex(self):
        for i in range(0, len(self.myList), 1):
            for j in range(0, len(self.myList[i]), 1):
                if self.myList[i][j] == 0:
                    return [i, j]

    def GetListIndex(self, someList):
        for i in range(0, len(someList), 1):
            if self.myList == someList[i].myList:
                return i
        return -1

    def __repr__(self):
        return repr((self.myList, self.myPreList, self.myCost))

    def GetGoalCost(self):
        sumCost = 9 * 100
        for i in range(0, len(self.myList), 1):
            for j in range(0, len(self.myList[i]), 1):
                if self.myList[i][j] == self.goal[i][j]:
                    sumCost -= 100
        return sumCost


def takeThr(elem):
    return elem.myCost


def checkNoAns(itlist):
    itsum = 0
    for i in range(0, len(itlist), 1):
        for j in range(0, len(itlist[i]), 1):
            for ii in range(0, i, 1):
                for jj in range(0, len(itlist[i]), 1):
                    if itlist[ii][jj] != 0 and itlist[i][j] != 0 and itlist[ii][jj] < itlist[i][j]:
                        itsum += 1
            for jj in range(0, j, 1):
                if itlist[i][jj] != 0 and itlist[i][j] != 0 and itlist[i][jj] < itlist[i][j]:
                    itsum += 1
    if itsum % 2 == 0:
        return True
    else:
        return False


def find0(alist):
    for i in range(3):
        for j in range(3):
            if alist[i][j] == 0:
                return i, j


# 用枚举类表示方向
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class NumberHuaRong(QWidget):
    """ 华容道主体 """

    def __init__(self):
        super().__init__()
        self.numbers = list(range(1, 10))
        self.blocks = []
        # 0的坐标
        self.zero_row = 0
        self.zero_column = 0
        self.rand = 0  # 缺的数字
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
        self.setWindowTitle('图片华容道')
        self.setWindowIcon(QIcon("图标.png"))
        # 设置背景颜色
        self.setStyleSheet("background-color:gray;")
        self.show()

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        global g_ListArr
        global g_readArr
        g_readArr = []
        g_ListArr = []
        self.ans = ""
        self.count = 0
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
        # self.goal = self.blocks.copy()
        # print(self.goal)
        # 打乱数组
        for i in range(100):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        self.mylist = self.blocks.copy()
        # print(self.mylist)
        self.updatePanel()

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            self.move(Direction.DOWN)
        if key == Qt.Key_Down or key == Qt.Key_S:
            self.move(Direction.UP)
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.move(Direction.RIGHT)
        if key == Qt.Key_Right or key == Qt.Key_D:
            self.move(Direction.LEFT)
        if key == Qt.Key_X:
            self.solve()
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
            if self.checkResult():
                if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战！'):
                    self.onInit()  # 结束后重新开始

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

    def getcost(self):
        self.cost = 0
        for row in range(3):
            for column in range(3):
                if row == self.zero_row and column == self.zero_column:
                    pass
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    self.cost = self.cost + 1
        return self.cost

    def prt(self):
        print("现在的状态：")
        print(self.blocks[0])
        print(self.blocks[1])
        print(self.blocks[2])
        print(self.getcost())

    '''def prt2(self, alist):
        print(alist[0])
        print(alist[1])
        print(alist[2])'''

    def solve(self):
        # self.prt2(self.mylist)
        self.goal = []
        for row in range(3):
            self.goal.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                self.goal[row].append(temp)
        # self.prt2(self.goal)
        self.mylist = self.blocks
        if not checkNoAns(self.mylist):
            print("No Ans!")
            exit(1)
        startNum = StruNum(self.mylist, [], 0, self.goal)
        g_ListArr.append(startNum)
        cichu = 0
        while g_ListArr:

            nowNum = g_ListArr[0]
            g_ListArr.remove(nowNum)  # 从队列头移除
            g_readArr.append(nowNum)  # 添加到已读队列
            cichu +=1;
            if nowNum.myList == self.goal:
                print("Find The Answer!")
                self.ans = ""
                while nowNum.myPreList:
                    x1, y1 = find0(nowNum.myList)
                    nowNum = nowNum.GetItsPre()
                    x2, y2 = find0(nowNum.myList)
                    if x2 > x1:
                        self.ans += "w"
                    elif x2 < x1:
                        self.ans += "s"
                    elif x2 == x1:
                        if y2 > y1:
                            self.ans += "a"
                        elif y2 < y1:
                            self.ans += "d"
                listans = list(self.ans)
                listans.reverse()
                self.ans = "".join(listans)
                print(self.ans)
                print(cichu)
                break
            else:
                [idx, jdx] = nowNum.GetZeroIndex()
                if idx - 1 >= 0:
                    upList = copy.deepcopy(nowNum.myList)
                    upList[idx][jdx] = upList[idx - 1][jdx]
                    upList[idx - 1][jdx] = 0
                    upNum = StruNum(upList, nowNum.myList, nowNum.myCost + 1, self.goal)
                    # A*算法：代价 = 到达此状态代价 + 期望到达目标节点代价
                    upNum.myCost += upNum.GetGoalCost()
                    # 如果新节点没有被走过
                    if upNum.GetListIndex(g_readArr) == -1:
                        tmpIndex = upNum.GetListIndex(g_ListArr)
                        if tmpIndex != -1:
                            # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                            if upNum.myCost < g_ListArr[tmpIndex].myCost:
                                g_ListArr.remove(g_ListArr[tmpIndex])
                                g_ListArr.append(upNum)
                        else:
                            g_ListArr.append(upNum)

                if idx + 1 < 3:
                    downList = copy.deepcopy(nowNum.myList)
                    downList[idx][jdx] = downList[idx + 1][jdx]
                    downList[idx + 1][jdx] = 0
                    downNum = StruNum(downList, nowNum.myList, nowNum.myCost + 1, self.goal)
                    downNum.myCost += downNum.GetGoalCost()
                    # 如果新节点没有被走过
                    if downNum.GetListIndex(g_readArr) == -1:
                        tmpIndex = downNum.GetListIndex(g_ListArr)
                        if tmpIndex != -1:
                            # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                            if downNum.myCost < g_ListArr[tmpIndex].myCost:
                                g_ListArr.remove(g_ListArr[tmpIndex])
                                g_ListArr.append(downNum)
                        else:
                            g_ListArr.append(downNum)

                if jdx - 1 >= 0:
                    leftList = copy.deepcopy(nowNum.myList)
                    leftList[idx][jdx] = leftList[idx][jdx - 1]
                    leftList[idx][jdx - 1] = 0
                    leftNum = StruNum(leftList, nowNum.myList, nowNum.myCost + 1, self.goal)
                    leftNum.myCost += leftNum.GetGoalCost()
                    # 如果新节点没有被走过
                    if leftNum.GetListIndex(g_readArr) == -1:
                        tmpIndex = leftNum.GetListIndex(g_ListArr)
                        if tmpIndex != -1:
                            # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                            if leftNum.myCost < g_ListArr[tmpIndex].myCost:
                                g_ListArr.remove(g_ListArr[tmpIndex])
                                g_ListArr.append(leftNum)
                        else:
                            g_ListArr.append(leftNum)

                if jdx + 1 < 3:
                    rightList = copy.deepcopy(nowNum.myList)
                    rightList[idx][jdx] = rightList[idx][jdx + 1]
                    rightList[idx][jdx + 1] = 0
                    rightNum = StruNum(rightList, nowNum.myList, nowNum.myCost + 1, self.goal)
                    rightNum.myCost += rightNum.GetGoalCost()
                    # 如果新节点没有被走过
                    if rightNum.GetListIndex(g_readArr) == -1:
                        tmpIndex = rightNum.GetListIndex(g_ListArr)
                        if tmpIndex != -1:
                            # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                            if rightNum.myCost < g_ListArr[tmpIndex].myCost:
                                g_ListArr.remove(g_ListArr[tmpIndex])
                                g_ListArr.append(rightNum)
                        else:
                            g_ListArr.append(rightNum)

                # 按照COST排序
                g_ListArr.sort(key=takeThr)


class Block(QLabel):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NumberHuaRong()
    sys.exit(app.exec_())
