#coding:utf-8
import requests
import json
import jsonpath

class Douban(object):

    def __init__(self):
        self.url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18'
        self.offset = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
            'Referer': 'https://m.douban.com/tv/american'
        }
        self.file = open('douban.json','w')

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self, data):
        dict_data = json.loads(data)

        # tv_list = dict_data['subject_collection_items']
        tv_list = jsonpath.jsonpath(dict_data, '$..subject_collection_items')[0]

        data_list = []

        for tv in tv_list:
            temp = {}

            # temp['title'] = tv['title']
            # temp['url'] = tv['url']

            temp['title'] = jsonpath.jsonpath(tv, 'title')
            temp['url'] = jsonpath.jsonpath(tv, 'url')
            data_list.append(temp)

        return data_list

    def save_data(self, data_list):
        for data in data_list:
            json_data = json.dumps(data, ensure_ascii=False) + ',\n'
            self.file.write(json_data)

    def __del__(self):
        self.file.close()

    def run(self):
        # 构建url
        # headers
        while True:
            # 发送请求获取响应
            url = self.url.format(self.offset)
            data = self.get_data(url)

            # 解析响应提取数据
            data_list = self.parse_data(data)

            # 保存
            self.save_data(data_list)

            if data_list == []:
                break
            else:
                self.offset += 18



if __name__ == '__main__':
    douban = Douban()
    douban.run()