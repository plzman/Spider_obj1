#coding:utf-8
from selenium import webdriver
import time

class Douyu(object):

    def __init__(self):
        self.url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()

    def parse_data(self):
        # 获取所有房间列表
        room_list = self.driver.find_elements_by_xpath('//*[@id="live-list-contentbox"]/li/a')

        data_list = []
        for room in room_list:
            temp = dict()
            temp['title'] = room.find_element_by_xpath('./div/div/h3').text
            temp['category'] = room.find_element_by_xpath('./div/div/span').text
            temp['owner'] = room.find_element_by_xpath('./div/p/span[1]').text
            temp['number'] = room.find_element_by_xpath('./div/p/span[2]').text
            temp['cover'] = room.find_element_by_xpath('./span/img').get_attribute('data-original')
            print(temp)
            data_list.append(temp)

        return data_list

    def save_data(self, data_list):
        pass

    # def __del__(self):
    #     self.driver.close()

    def run(self):
        # url
        # 发送请求获取响应
        self.driver.get(self.url)

        while True:
            # 解析
            data_list = self.parse_data()
            # 保存
            self.save_data(data_list)

            # 翻页
            try:
                el_next = self.driver.find_element_by_xpath('//a[@class="shark-pager-next"]')
                el_next.click()
                time.sleep(3)
            except:
                break



if __name__ == '__main__':
    douyu = Douyu()
    douyu.run()