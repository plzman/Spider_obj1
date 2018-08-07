#coding:utf-8
import requests


class Tieba(object):

    def __init__(self, name, pn):
        self.name = name
        self.base_url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn='.format(name)
        self.url_list = [self.base_url + str(p*50) for p in range(pn)]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

    def get_data(self, url):
        res = requests.get(url,headers=self.headers)
        return res.content

    def save_data(self, data, index):
        filename = self.name + '_{}.html'.format(index)

        with open(filename, 'wb')as f:
            f.write(data)

    def run(self):
        # 构建url
        # 构建批量的url
        # 遍历链接列表
        for url in self.url_list:
            index = self.url_list.index(url)
            # 发送请求，获取响应
            data = self.get_data(url)
            # 保存
            self.save_data(data, index)
        pass

if __name__ == '__main__':
    tieba = Tieba('非诚勿扰',3)
    tieba.run()