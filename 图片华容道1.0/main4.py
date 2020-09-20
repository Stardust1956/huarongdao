#把数字改为图片

import sys
import random
from enum import IntEnum
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QIcon, QPixmap
from PyQt5.QtCore import Qt
import cv2

import numpy
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
        self.blocks = []
        #0的坐标
        self.zero_row = 0
        self.zero_column = 0
        self.rand = 0 #缺的数字
        self.gltMain = QGridLayout()

        self.initUI()

    def initUI(self):
        # 设置方块间隔
        self.gltMain.setSpacing(10)

        self.onInit()

        # 设置布局
        self.setLayout(self.gltMain)
        # 设置宽和高
        self.setFixedSize(950,950)
        # 设置标题和图标
        self.setWindowTitle('图片华容道')
        self.setWindowIcon(QIcon("图标.png"))
        # 设置背景颜色
        self.setStyleSheet("background-color:gray;")
        self.show()

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        self.rand = random.randint(1, 9)  # 缺的数字
        # print("rand ",self.rand)
        self.numbers = list(range(1, 10))
        self.numbers[self.rand-1] = 0
        # print("numbers ",self.numbers)
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
        # print("blocks ",self.blocks)#[[1, 2, 3], [4, 5, 6], [7, 0, 9]]
        # 打乱数组
        for i in range(50):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))

        self.updatePanel()

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_Up or key == Qt.Key_W):
            self.move(Direction.DOWN)
        if (key == Qt.Key_Down or key == Qt.Key_S):
            self.move(Direction.UP)
        if (key == Qt.Key_Left or key == Qt.Key_A):
            self.move(Direction.RIGHT)
        if (key == Qt.Key_Right or key == Qt.Key_D):
            self.move(Direction.LEFT)
        self.updatePanel()
        if self.checkResult():
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战！'):
                self.onInit()  # 结束后重新开始

    # 方块移动算法
    def move(self, direction):
        if(direction == Direction.UP): # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if(direction == Direction.DOWN): # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if(direction == Direction.LEFT): # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if(direction == Direction.RIGHT): # 右
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
        # 先检测最右下角是否为0
        if self.blocks[self.zero_row][self.zero_column] != 0:
            return False

        for row in range(3):
            for column in range(3):
                if row == self.zero_row and column == self.zero_column:
                    pass
                #值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

        return True
        # flag = 0
        # for row in range(3):
        #     for colum in range(3):
        #         if self.blocks[row][colum] != row * 3 + colum +1:
        #             flag += 1
        # if flag == 1:
        #     return True
        # return False

class Block(QLabel):
    """ 数字方块 """

    def __init__(self, number):
        super().__init__()
        self.imgPath = ["sub" + str(i) + ".png" for i in range(1, 10)]
        self.number = number
        self.setFixedSize(300, 300)#控制窗体大小
        if self.number > 0:
        # 导入图片
        #     img = cv2.imread("sub1.png")
            imgName = self.imgPath[number-1]
            pix = QPixmap(imgName)
            lb1 = QLabel(self)
            lb1.setPixmap(pix)
        # # 设置字体
        # font = QFont()
        # font.setPointSize(50)
        # font.setBold(True)
        # self.setFont(font)
        #
        # # 设置字体颜色
        # pa = QPalette()
        # pa.setColor(QPalette.WindowText, Qt.white)
        # self.setPalette(pa)
        #
        # # 设置文字位置
        # self.setAlignment(Qt.AlignCenter)

        # 设置背景颜色\圆角和文本内容
        if self.number == 0:
            self.setStyleSheet("background-color:white;border-radius:10px;")
        # else:
        #     self.setStyleSheet("background-color:red;border-radius:10px;")
        #     self.setText(str(self.number))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NumberHuaRong()
    sys.exit(app.exec_())