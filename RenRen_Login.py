#coding:utf-8
import requests
import json
import js2py
import re

def login():

    # 发送第一个ajax请求获取公钥数据
    ajax_url_1 = 'http://activity.renren.com/livecell/rKey'
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
    }
    data = session.get(ajax_url_1).content.decode()
    print(data)


    # 构建js执行的环境
    context = js2py.EvalJs()

    # 添加RSA.js
    rsa_js = session.get('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/RSA.js').content.decode()
    context.execute(rsa_js)

    # 添加BIGINT.js
    bigint_js = session.get('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/BigInt.js').content.decode()
    context.execute(bigint_js)

    # 添加Barrett.js
    barrett_js = session.get('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/Barrett.js').content.decode()
    context.execute(barrett_js)

    # 添加t
    context.t = {
        'phonenum’:’手机号’,
        'password’:’密码’,
        'c1': 0
    }
    # 添加n
    context.n = json.loads(data)['data']

    # 添加执行加密代码
    pwd_js = """
        t.password = t.password.split("").reverse().join(""),
        setMaxDigits(130);
        var o = new RSAKeyPair(n.e,"",n.n)
          , r = encryptedString(o, t.password);
        t.password = r,
        t.rKey = n.rkey
    """
    context.execute(pwd_js)

    print(context.t)

    # 从执行环境中获取post数据
    post_data = context.t.to_dict()
    print(post_data)

    # 向登录url发送登录请求
    ajax_url_2 = 'http://activity.renren.com/livecell/ajax/clog'
    session.post(ajax_url_2, data=post_data)

    # 验证登录状态
    res = session.get('http://activity.renren.com/myprofile')

    print(res.url)

if __name__ == '__main__':
    login()