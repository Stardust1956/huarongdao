import base64
import json
import cv2
import requests
import quedinxulie


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


def getproblem():
    url = "http://47.102.118.1:8089/api/problem?stuid=031802418"
    # 每次请求的结果都不一样，动态变化
    text = json.loads(gethtml(url))
    img_base64 = text["img"]
    step = text["step"]
    swap = text["swap"]
    uuid = text["uuid"]
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


def getAnswer(url, data_json):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Content-Type': 'application/json'
    }
    r = requests.post(url, headers=headers, data=data_json)
    return r.text


def submit(uuid, operations, swap):
    url = " http://47.102.118.1:8089/api/answer"
    data = {"uuid": uuid, "answer": {"operations": operations, "swap": swap}}
    data_json = json.dumps(data)
    ret = getAnswer(url, data_json)
    ret2 = json.loads(ret)
    answer = ret2['answer']
    score = ret2['score']
    time = ret2['time']
    print('answer:', answer)
    print('score:', score)
    print('time:', time)

