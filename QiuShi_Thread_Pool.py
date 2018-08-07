#coding:utf-8
import requests
from lxml import etree
import json
import time
from multiprocessing.dummy import Pool
from queue import Queue

class Qiushi(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.file = open('qiushi.json', 'w')
        self.pool = Pool()
        self.queue = Queue()
        self.request_num = 0
        self.response_num = 0
        self.is_running = True

    def generate_url_list(self):
        print('正在生成url队列')
        # return [self.url.format(i) for i in range(1,14)]

        for i in range(1, 14):
            url = self.url.format(i)
            self.queue.put(url)
            self.request_num += 1

    def get_data(self, url):
        print('正在获取{}对应的响应'.format(url))
        response = requests.get(url, headers=self.headers)
        if response.status_code == 503:
            self.queue.put(url)
            return None
        else:
            return response.content

    def parse_data(self, data):
        # 将源码创建成element对象
        html = etree.HTML(data)
        print('正在解析')
        # 获取帖子节点列表
        el_list = html.xpath('//div[@id="content-left"]/div')

        data_list = []
        # 遍历帖子节点列表
        for el in el_list:
            temp = {}
            temp['content'] = el.xpath('./a/div/span/text()')[0].strip()
            data_list.append(temp)
            # print(temp)
        return data_list

    def save_data(self, data_list):
        print('正在保存')
        for data in data_list:
            json_data = json.dumps(data,ensure_ascii=False) + ',\n'
            self.file.write(json_data)

    def _request_response_data(self):
        url = self.queue.get()
        # 发送秦秋获取响应
        data = self.get_data(url)
        if data == None:
            return
        # 解析响应
        data_list = self.parse_data(data)

        # 保存
        self.save_data(data_list)
        self.response_num += 1

    def _callback(self, temp):
        if self.is_running:
            self.pool.apply_async(self._request_response_data, callback=self._callback)

    def __del__(self):
        self.file.close()

    def run(self):

        self.generate_url_list()

        # 从线程池中申请一个线程执行方法
        for i in range(4):
            self.pool.apply_async(self._request_response_data, callback=self._callback)

        while True:
            if self.request_num == self.response_num:
                self.is_running = False
                break

        self.pool.close()




if __name__ == '__main__':
    qiushi = Qiushi()

    start = time.time()
    qiushi.run()
    end = time.time()
    print(end-start)