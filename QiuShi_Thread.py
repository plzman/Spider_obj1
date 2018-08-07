#coding:utf-8
import requests
from lxml import etree
import json
import time
import threading
from queue import Queue


class Qiushi(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.file = open('qiushi.json', 'w')
        self.url_queue = Queue()
        self.response_queue = Queue()
        self.data_queue = Queue()

    def generate_url_list(self):
        print('正在生成url队列')
        # return [self.url.format(i) for i in range(1,14)]

        for i in range(1, 14):
            url = self.url.format(i)
            self.url_queue.put(url)

    def get_data(self):
        while True:
            url = self.url_queue.get()
            print('正在获取{}对应的响应'.format(url))
            response = requests.get(url, headers=self.headers)
            if response.status_code == 503:
                self.url_queue.put(url)
            else:
                self.response_queue.put(response.content)
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            data = self.response_queue.get()
            print('正在解析')
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
                # print(temp)
            self.data_queue.put(data_list)
            self.response_queue.task_done()

    def save_data(self):
        while True:
            print('正在保存')
            data_list = self.data_queue.get()
            for data in data_list:
                json_data = json.dumps(data,ensure_ascii=False) + ',\n'
                self.file.write(json_data)
            self.data_queue.task_done()

    def __del__(self):
        self.file.close()

    def run(self):
        # # url
        # # url_list
        # url_list = self.generate_url_list()
        # # headers
        # # 遍历url_list
        # for url in url_list:
        #
        #     # 发送秦秋获取响应
        #     data = self.get_data(url)
        #
        #     # 解析响应
        #     data_list = self.parse_data(data)
        #
        #     # 保存
        #     self.save_data(data_list)

        thread_list = []

        # 创建线程
        t_generate_list = threading.Thread(target=self.generate_url_list)
        thread_list.append(t_generate_list)

        # 创建发送请求的线程
        for i in range(4):
            t = threading.Thread(target=self.get_data)
            thread_list.append(t)

        # 创建解析响应的线程
        for i in range(3):
            t = threading.Thread(target=self.parse_data)
            thread_list.append(t)

        t_save_data = threading.Thread(target=self.save_data)
        thread_list.append(t_save_data)

        # 设置并启动线程
        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.url_queue,self.response_queue,self.data_queue]:
            q.join()

if __name__ == '__main__':
    qiushi = Qiushi()

    start = time.time()
    qiushi.run()
    end = time.time()
    print(end-start)