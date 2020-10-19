import base64
import json
import cv2
import requests

import quedinxulie


def mypost(url, data_json):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Content-Type': 'application/json'
    }
    r = requests.post(url, headers=headers, data=data_json)
    return r.text


def gethtml(url):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36'
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getAllProblems():
    # 获取所有赛题
    url = "http://47.102.118.1:8089/api/challenge/list"
    datas = json.loads(gethtml(url))
    # print(data)#列表
    i = 0
    for data in datas:

        print("第" + str(i) + "道题")
        i += 1
        for key in data.keys():
            print(key + " = ", data[key])

        print("______________________________________")


def getAnswers(uuid):
    # 获取赛题的解题记录
    url = "http://47.102.118.1:8089/api/challenge/record/" + str(uuid)
    datas = json.loads(gethtml(url))
    # print(datas)#列表
    i = 0
    print("uuid = ", uuid)
    for data in datas:
        print("第" + str(i) + "名")
        i += 1
        for key in data.keys():
            print(key + " = ", data[key])
        print("______________________________________")


def creatProblem( letter, exclude, challenge, step):
    # 创建赛题
    url = "http://47.102.118.1:8089/api/challenge/create"
    datas = {
        "teamid": 22,
        "data": {
            "letter": letter,
            "exclude": exclude,
            "challenge": challenge,
            "step": step,
            "swap": [1, 2],
        },
        "token": "5f1aaa82-8261-4e72-8c95-f96f83f64548"
    }
    data_json = json.dumps(datas)
    ret = json.loads(mypost(url, data_json))
    for key in ret.keys():
        print(key + " : ", ret[key])


def getRank():
    # 获取排行榜
    url = "http://47.102.118.1:8089/api/rank"
    datas = json.loads(gethtml(url))
    i = 1
    for data in datas:
        print("第" + str(i) + "名")
        i += 1
        for key in data.keys():
            print(key + " = ", data[key])
        print("______________________________________")


def getTeamDetail():
    # 获取队伍详细信息
    url = "http://47.102.118.1:8089/api/teamdetail/" + str(22)
    datas = json.loads(gethtml(url))
    print("team : ", 22)
    for key in datas.keys():
        print(key + " = ", datas[key])
    print("______________________________________")


def challenge(uuid):
    # 挑战赛题的接口,获取赛题
    url = "http://47.102.118.1:8089/api/challenge/start/" + uuid
    inputdata = {
        "teamid": 22,
        "token": "5f1aaa82-8261-4e72-8c95-f96f83f64548"
    }
    data_json = json.dumps(inputdata)
    ret = json.loads(mypost(url, data_json))
    print("剩余次数 = ", ret["chanceleft"])
    print("uuid = ", ret["uuid"])
    uuid = ret["uuid"]
    print("答题倒计时 = ", ret["expire"])
    print("success = ", ret["success"])
    data = ret["data"]
    # print(data.keys())#dict_keys(['img', 'step', 'swap'])
    img_base64 = data["img"]
    step = data["step"]
    swap = data["swap"]
    img = base64.b64decode(img_base64)
    # 获取接口的图片并写入本地
    with open("photo.jpg", "wb") as fp:
        fp.write(img)  # 900*900
    # 切分图片，切成9张
    img = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)
    for row in range(3):
        for colum in range(3):
            sub = img[row * 300:(row + 1) * 300, colum * 300:(colum + 1) * 300]
            # print(sub.shape)
            cv2.imwrite("Getsub" + str(row * 3 + colum + 1) + ".jpg", sub)
    # 映射图片，因为得到的图片顺序是未知的，所以需要一个映射把图片的顺序弄正确，这一部分还没完成
    zuhao, alist, disnumber = quedinxulie.getlist()
    return step, swap, uuid, zuhao, alist, disnumber


def submit(uuid, operations, swap):
    # 提交代码
    url = "http://47.102.118.1:8089/api/challenge/submit"
    inputdata = {
        "uuid": uuid,
        "teamid": 22,
        "token": "5f1aaa82-8261-4e72-8c95-f96f83f64548",
        "answer": {
            "operations": operations,
            "swap": swap
        }
    }

    data_json = json.dumps(inputdata)
    ret = json.loads(mypost(url, data_json))
    for key in ret.keys():
        print(key + " = ", ret[key])

def solveall():
    # 获取所有赛题
    url = "http://47.102.118.1:8089/api/team/problem/22"
    datas = json.loads(gethtml(url))
    return datas


def getUnfinishProblems():
    # 获取未解决的赛题
    url = "http://47.102.118.1:8089/api/team/problem/22"
    datas = json.loads(gethtml(url))
    # print(data)#列表
    i = 1
    for data in datas:
        print("第"+str(i)+"道题")
        i += 1
        for key in data.keys():
            print(key+" = ", data[key])
        print("______________________________________")