"""import base64
import cv2
path = "D://zhifu/"
for i in range(36):
    path1 = path+str(i)+".jpg"
# 切分图片，切成9张
    img = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    for row in range(3):
        for colum in range(3):
            sub = img[row * 300:(row + 1) * 300, colum * 300:(colum + 1) * 300]
            cv2.imwrite(str(i) + '_' + str(row * 3 + colum + 1) + ".jpg", sub)
def rename():
    path = "D://0作业/软工实践/hrd/无框字符"
    filelist = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
    count = 0
    for files in filelist:  # 遍历所有文件
        Olddir = os.path.join(path, files)  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue
        filename = os.path.splitext(files)[0]  # 文件名
        filetype = os.path.splitext(files)[1]  # 文件扩展名
        Newdir = os.path.join(path, '{0}'.format(count) + filetype)  # 新的文件路径
        count += 1
        os.rename(Olddir, Newdir)  # 重命名
rename()"""
from PIL import Image
from PIL import ImageChops


def compare_images(path_one, path_two):
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
    try:
        diff = ImageChops.difference(image_one, image_two)

        if diff.getbbox() is None:
            return True
        else:
            return False

    except ValueError as e:
        return "{0}\n{1}".format(e, "图片大小和box对应的宽度不一致!")


def getzu(path11):
    path = 'D://0作业/软工实践/hrd/确定序列/'
    for i in range(36):
        path2 = path + str(i) + '_'
        for j in range(1, 10):
            path22 = path2 + str(j) + '.jpg'
            if compare_images(path11, path22):
                return i


def getxulie(zuhao):
    listnow = []
    for i in range(1, 10):
        path11 = 'D://0作业/软工实践/hrd/图片华容道1.0/' + "Getsub" + str(i) + ".jpg"
        if compare_images(path11, 'white.jpg'):
            listnow.append(0)
        else:
            for j in range(1, 10):
                path22 = 'D://0作业/软工实践/hrd/确定序列/' + str(zuhao) + '_' + str(j) + ".jpg"
                if compare_images(path11, path22):
                    listnow.append(j)
    disnumber = 0
    listnowsum = 0
    for i in listnow:
        listnowsum += int(i)
        disnumber = 45 - listnowsum
    listnow2 = [[], [], []]
    listnow2[0] = listnow[0:3]
    listnow2[1] = listnow[3:6]
    listnow2[2] = listnow[6:9]
    return listnow2, disnumber


def getlist():
    path1 = ''
    zimu = 'aabbcddefghhjkmmnooppqqrstuuvwxxyyzz'
    for i in range(1, 10):
        filename = 'D://0作业/软工实践/hrd/图片华容道1.0/' + "Getsub" + str(i) + ".jpg"
        if not compare_images(filename, 'white.jpg'):
            if not compare_images(filename, 'black.jpg'):
                path1 = filename
                break
    zuhao = getzu(path1)
    alist, disnumber = getxulie(zuhao)
    print("该图是第{0}张图片".format(zuhao))
    print("对应字母为：", zimu[zuhao])
    print("题目序列是")
    print(alist[0])
    print(alist[1])
    print(alist[2])
    return zuhao, alist, disnumber
