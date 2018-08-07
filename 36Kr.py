#coding:utf-8
import requests
import re
import json


class Kr36(object):

    def __init__(self):
        self.url = 'http://36kr.com/'
        self.ajax_url = 'http://36kr.com/api/search-column/mainsite?per_page=20&page={}'
        self.offset = 2
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.file = open('36kr.json', 'w')

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_data(self, data):
        temp = re.findall(' <script>var props=({.*})</script>', data)[0]

        temp = temp.split(',locationnal=')[0]


        # 将提取到的json字符串转换成Python字典
        dict_data = json.loads(temp)

        news_list = dict_data['feedPostsLatest|post']

        data_list = []

        for news in news_list:
            temp = {}
            temp['title'] = news['title']
            temp['url'] = news['cover']
            data_list.append(temp)

        return data_list

    def parse_ajax_data(self, data):
        dict_data = json.loads(data)

        news_list = dict_data['data']['items']

        data_list = []

        for news in news_list:
            temp = {}
            temp['title'] = news['title']
            temp['url'] = news['cover']
            data_list.append(temp)

        return data_list

    def save_data(self, data_list):
        for data in data_list:
            json_data = json.dumps(data, ensure_ascii=False) + ',\n'
            self.file.write(json_data)

    def __del__(self):
        self.file.close()

    def run(self):
        # 首页url
        # headers
        # 发请求获取响应
        data = self.get_data(self.url)

        # 正则解析
        data_list = self.parse_data(data)

        # 保存
        self.save_data(data_list)

        while True:
            # ajax——url
            url = self.ajax_url.format(self.offset)
            # 发请求获取响应
            data = self.get_data(url)

            # json解析
            data_list = self.parse_ajax_data(data)

            # 保存
            self.save_data(data_list)

            # 检查循环终止条件拼接url
            if data_list == []:
                break
            else:
                self.offset += 1

if __name__ == '__main__':
    kr36 = Kr36()
    kr36.run()