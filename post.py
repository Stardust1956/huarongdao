
import json
import requests

def getAnswer(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
            'Content-Type': 'application/json'
        }
        r=requests.post(url,headers = headers,data = data_json)
        return r.text

if __name__ == "__main__":
    url = " http://47.102.118.1:8089/api/answer"
    #提交的数据，
    # uuid: 题目的标识
    # operations：你的操作序列
    # swap：你自由调换操作的图片编号
    data = {
    "uuid":"20c8d3e27d6e4d638a1fed4218737e41",#本道题目标识
    "answer":{
        "operations": "wsaaadasdadadaws",
        "swap": [1,2]
            }
            }
    data_json = json.dumps(data)#转为json提交
    # print(data_json)
    ret = getAnswer(url)
    print(ret)
    # score: 是否通过测试
    # time：耗时(秒）