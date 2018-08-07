#coding:utf-8
import requests
from lxml import etree
import os

class Tieba(object):

    def __init__(self, name):
        self.url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=0'.format(name)
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0) '
        }

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_list_page(self, data):
        # 将源码转换成element对象
        html = etree.HTML(data)

        # 提取标题对象列表
        el_list = html.xpath('//li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a')
        data_list = []
        # 遍历标题节点列表，从每一特节点中抽取标题和链接
        for el in el_list:
            temp = {}
            temp['title'] = el.xpath('./text()')[0]
            temp['link'] = 'https://tieba.baidu.com' + el.xpath('./@href')[0]
            data_list.append(temp)
            # print(temp)

        # 获取下一页url
        try:
            next_url = 'https:' + html.xpath('//a[contains(text(),"下一页>")]/@href')[0]
        except:
            next_url = None

        return data_list, next_url

    def parse_detail_page(self, data):
        # 将源码转换成element对象
        html = etree.HTML(data)

        image_list = html.xpath('//img[@class="BDE_Image"]/@src')

        return image_list

    def downloader(self, image_list):
        if not os.path.exists('images'):
            os.mkdir('images')

        for url in image_list:
            print(url)
            data = self.get_data(url)
            filename = 'images' + os.sep + url.split('/')[-1]
            with open(filename, 'wb')as f:
                f.write(data)

    def run(self):
        # url
        # headers
        url = self.url
        while True:
            # 发起列表页面的请求
            data = self.get_data(url)
            print(data)
            # 解析列表页面响应(详情页面url和标题列表&下一页url)
            detail_list, url = self.parse_list_page(data)
            print(url)
            # 遍历详情页面url和标题列表
            for detial in detail_list:
                # 获取详情页面的url
                detail_url = detial['link']
                # 发送详情页面url请求
                detail_data = self.get_data(detail_url)
                # 从详情页面的响应中解析出图片地址列表
                image_list = self.parse_detail_page(detail_data)
                # 下载
                self.downloader(image_list)
            # 判断循环终止条件
            if url == None:
                break

if __name__ == '__main__':
    tieba = Tieba('李毅')
    tieba.run()