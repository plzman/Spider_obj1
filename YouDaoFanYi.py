#coding:utf-8
import requests
import time
import hashlib
import random
import json


class Youdao(object):

    def __init__(self, word):
        self.word = word
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/?keyfrom=dict2.index',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-1392948312@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=1507578365.437866; _ntes_nnid=3186e433d683814b1b9d1c6b5e1f803f,1530331087164; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abczhPECatcy6hVbOEktw; fanyi-ad-id=47865; fanyi-ad-closed=1; ___rl__test__cookies=1532426143369'
        }
        self.post_data = None

    def generate_post_data(self):
        # r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
        now = int(time.time()*1000)
        randint = random.randint(0,9)
        r = str(now + randint)

        # o = u.md5(S + n + r + D)
        S = "fanyideskweb"
        n = self.word
        D = "ebSeFb%=XZ%T[KZ)c(sy!"
        tempstr = S + n + r + D

        # 创建md5对象
        md5 = hashlib.md5()

        # 添加需要hash运算的数据,python3需要填装bytes
        md5.update(tempstr.encode())

        # 获取hash值
        o = md5.hexdigest()

        self.post_data = {
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": r,
            "sign": o,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_CLICKBUTTION",
            "typoResult": False,
        }

    def get_data(self):
        response = requests.post(self.url, headers=self.headers, data=self.post_data)
        return response.content.decode()

    def parse_data(self,data):
        result = json.loads(data)['translateResult'][0][0]['tgt']
        print(result)

    def run(self):
        # url
        # headers
        # post_data
        self.generate_post_data()
        print(self.post_data)
        # 发请求
        data = self.get_data()
        # 解析
        self.parse_data(data)

if __name__ == '__main__':
    youdao = Youdao('我让你给我翻译一下百度用英语怎么说')
    youdao.run()