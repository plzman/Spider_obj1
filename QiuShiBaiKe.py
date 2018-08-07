#coding:utf-8
import requests
from lxml import etree
import json
import time
class Qiushi(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.file = open('qiushi.json', 'w')

    def generate_url_list(self):
        return [self.url.format(i) for i in range(1,14)]

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self, data):
        # 将源码创建成element对象
        html = etree.HTML(data)

        # 获取帖子节点列表
        el_list = html.xpath('//div[@id="content-left"]/div')

        data_list = []
        # 遍历帖子节点列表
        for el in el_list:
            temp = {}
            temp['content'] = el.xpath('./a/div/span/text()')[0].strip()
            data_list.append(temp)
            print(temp)
        return data_list

    def save_data(self, data_list):
        for data in data_list:
            json_data = json.dumps(data,ensure_ascii=False) + ',\n'
            self.file.write(json_data)

    def __del__(self):
        self.file.close()

    def run(self):
        # url
        # url_list
        url_list = self.generate_url_list()
        # headers
        # 遍历url_list
        for url in url_list:

            # 发送秦秋获取响应
            data = self.get_data(url)

            # 解析响应
            data_list = self.parse_data(data)

            # 保存
            self.save_data(data_list)

if __name__ == '__main__':
    qiushi = Qiushi()

    start = time.time()
    qiushi.run()
    end = time.time()
    print(end-start)