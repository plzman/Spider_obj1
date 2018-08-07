#coding:utf-8
from selenium import webdriver
import requests
from yundama import identify

dr = webdriver.Chrome()
dr.get('https://accounts.douban.com/login')


# 账号
el_user = dr.find_element_by_id('email')
el_user.send_keys('m17173805860@163.com')

# 密码
el_user = dr.find_element_by_id('password')
el_user.send_keys('1qaz@WSX3edc')

# 下载图片验证码
el_user = dr.find_element_by_id('captcha_image')
url = el_user.get_attribute('src')
data = requests.get(url).content


# 解析并输入验证码
result = identify(data)
el_user = dr.find_element_by_id('captcha_field')
el_user.send_keys(result)

# 点击登录
el_user = dr.find_element_by_name('login')
el_user.click()