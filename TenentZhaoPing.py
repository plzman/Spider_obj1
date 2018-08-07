#coding:utf-8
import requests
from bs4 import BeautifulSoup

class Tencent(object):

    def __init__(self):
        self.url = 'https://hr.tencent.com/position.php'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self, data):
        # 创建对象
        soup = BeautifulSoup(data,'lxml')


        data_list = []
        el_list = soup.select('.odd,.even')
        # print(len(el_list))
        for el in el_list:
            temp = {}
            temp['name'] = el.select('td a')[0].get_text()
            temp['link'] = el.select('td a')[0].get('href')
            temp['category'] = el.select('td')[1].get_text()
            temp['num'] = el.select('td')[2].get_text()
            temp['address'] = el.select('td')[3].get_text()
            temp['date'] = el.select('td')[4].get_text()

            data_list.append(temp)

        # 下一页url
        next_url = 'https://hr.tencent.com/' + soup.select('#next')[0].get('href')

        return data_list,next_url

    def run(self):
        # url
        # headers
        url = self.url
        while True:
            # 发请求
            data = self.get_data(url)
            # 解析
            data_list, url = self.parse_data(data)
            # 保存
            for data in data_list:
                print(data)
            # 翻页
            if 'javascript:;' in url:
                break

if __name__ == '__main__':
    tencent = Tencent()
    tencent.run()