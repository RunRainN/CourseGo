# -*- coding:utf-8 -*-

import requests
import time

session = requests.session()
t = int(round(time.time() * 1000))  # 获取unix时间戳
headers = {"Host": "jwxt.cumt.edu.cn",
           "Connection": "keep-alive",
           # "Content-Length":"470",
           "Cache-Control": "max-age=0",
           "Origin": "http://jwxt.cumt.edu.cn",
           "Upgrade-Insecure-Requests": "1",
           "Content-Type": "application/x-www-form-urlencoded",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
           "Referer": "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=" + str(t),
           # "Accept-Encoding":"gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9"
           }


def get_captcha():
    captcha_url = "http://jwxt.cumt.edu.cn/jwglxt/kaptcha"
    for i in range(5000):
        try:
            captcha = session.get(captcha_url, headers=headers).content
        except Exception as e:
            print(u"连接失败，正在重连...")
            get_captcha()
        with open(".\captcha_pictures\captcha_" + str(i) + ".jpeg", "wb") as f:
            f.write(captcha)
        print(i)
        time.sleep(1)


get_captcha()
