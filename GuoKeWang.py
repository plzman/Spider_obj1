#coding:utf-8
import requests
import re
import json

class Guokr(object):

    def __init__(self):
        self.url = 'https://www.guokr.com/ask/highlight/?page=1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.file = open('guokr.json', 'w')

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_data(self, data):

        results = re.findall('<h2><a target="_blank" href="(.*)">(.*)</a></h2>', data)

        data_list = []

        for result in results:
            temp = {}
            temp['title'] = result[-1]
            temp['url'] = result[0]
            data_list.append(temp)

        # 提取下一页链接
        next_url = re.findall('<a href="(/ask/highlight/\?page=\d+)">下一页</a>', data)

        return data_list, next_url

    def save_data(self, data_list):
        for data in data_list:
            json_data = json.dumps(data, ensure_ascii=False) + ',\n'
            self.file.write(json_data)

    def __del__(self):
        self.file.close()


    def run(self):
        # url
        # headers
        url = self.url
        while True:
            # 发送请求获取响应
            data = self.get_data(url)
            # print(data)

            # 从响应中提取数据
            data_list, next_url = self.parse_data(data)

            # 保存
            self.save_data(data_list)
            # 判断是否到结尾，不到结尾构造下一页链接

            if next_url == []:
                break
            else:
                url = 'https://www.guokr.com/' + next_url[0]

if __name__ == '__main__':
    guokr = Guokr()
    guokr.run()