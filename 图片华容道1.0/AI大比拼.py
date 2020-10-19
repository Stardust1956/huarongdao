# coding:utf-8
# 957820341
import copy
import jiekou
from enum import IntEnum

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


class NumberHuaRong():
    """ 华容道主体 """

    def __init__(self):
        super().__init__()
        self.numbers = list(range(1, 10))
        self.blocks = []
        # 0的坐标
        self.zero_row = 0
        self.zero_column = 0
        self.disnum = 0  # 缺的数字位置
        self.cost = 0
        self.mylist = []
        self.goal = []
        self.ans = ""
        self.count = 0
        self.onInit()

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

        self.mylist = self.blocks.copy()
        self.solve()

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
            print('无解，进行用户交换{0}：'.format([flag1 + 1, flag2 + 1]))
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
            print(self.zero_row, self.zero_column)
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


if __name__ == '__main__':
    while 1:
        print("1 获取赛题 2 获取赛题解题记录 3 创建赛题 4 挑战赛题 5 查看未挑战赛题 6 查看所有队伍排名 7查看我的队伍信息 8 一键解题")
        operation = int(input("请输入你要的操作："))
        if operation == 1:
            jiekou.getAllProblems()
        elif operation == 2:
            uuid = input("请输入uuid：")
            jiekou.getAnswers(uuid)
        elif operation == 3:
            letter = input("请输入字母：")
            exclude = int(input("请输入哪个位置为0："))
            challenge = [[6, 4, 7], [8, 5, 0], [3, 2, 1]]
            step = int(input("请输入强制交换步数："))
            jiekou.creatProblem(letter, exclude, challenge, step)
        elif operation == 4:
            uuid = input("请输入要挑战赛题的uuid：")
            step, swap, uuid, zuhao, listproblem, dis = jiekou.challenge(uuid)
            set(step, swap, uuid, zuhao, listproblem, dis)
            NumberHuaRong()
            jiekou.submit(uuid, operations, myswap)
            print("operations=", operations)
            print("myswap=", myswap)
        elif operation == 5:
            jiekou.getUnfinishProblems()
        elif operation == 6:
            jiekou.getRank()
        elif operation == 7:
            jiekou.getTeamDetail()
        elif operation == 8:
            datas = jiekou.solveall()
            i = 0
            for data in datas:
                print("第" + str(i) + "道题")
                i += 1
                uuid = data["uuid"]
                if uuid =="9550c051-5b66-4467-9da5-0d9648405925":
                    continue
                else:
                    step, swap, uuid, zuhao, listproblem, dis = jiekou.challenge(uuid)
                    set(step, swap, uuid, zuhao, listproblem, dis)
                    NumberHuaRong()
                    jiekou.submit(uuid, operations, myswap)
                    print("operations=", operations)
                    print("myswap=", myswap)
                    print("______________________________________")
        '''elif operation == 10:
            uuid1 = input("请输入要挑战赛题的uuid：")
            step, swap, uuid, zuhao, listproblem, dis = jiekou.challenge(uuid1)
            set(step, swap, uuid, zuhao, listproblem, dis)
            NumberHuaRong()
            jiekou.submit(uuid, operations, myswap)
            print("uuid= ", uuid1)
            print("list= ", listproblem)
            print("step= ", step)
            print("swap= ", swap)
            print("operations= ", operations)
            print("myswap = ", myswap)
        elif operation == 11:
            step = 20
            swap = [1, 2]
            listproblem = [[6, 4, 7], [8, 5, 0], [3, 2, 1]]
            zuhao = 1
            dis = 9
            uuid = "1"
            set(step, swap, uuid, zuhao, listproblem, dis)
            NumberHuaRong()
            print("operations= ", operations)
            print("myswap = ", myswap)'''




