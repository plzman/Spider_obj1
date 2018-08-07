#coding:utf-8
import requests
import json


class King(object):

    def __init__(self, word):
        self.url = 'http://fy.iciba.com/ajax.php?a=fy'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.post_data = {
            "f": "auto",
            "t": "auto",
            "w": word
        }

    def get_data(self):
        response = requests.post(self.url, headers=self.headers, data=self.post_data)
        return response.content

    def parse_data(self, data):
        dict_data = json.loads(data)
        try:
            print(dict_data['content']['out'])
        except:
            print(dict_data['content']['word_mean'])

    def run(self):
        # url
        # headers
        # post_data
        # 发送请求获取响应
        data = self.get_data()
        # print(data)
        # 解析
        self.parse_data(data)


if __name__ == '__main__':
    king = King('China')
    king.run()