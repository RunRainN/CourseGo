# -*- coding:utf-8 -*-
"""
mail : 1121192423@qq.com
"""

import requests
import time
import os
import base64
import lxml.html
import RSAJS
from hex2b64 import HB64
from fuction import FunctionMenu
import hashlib
import getpass
import re


class EducationalAdministrationSystem:
    # 初始化
    def __init__(self):
        print("-" * 25)
        print(u"程序名：CourseGo")
        print(u"版本：1.7")
        print(u"时间：2020.7")
        print(u"语言：Python 2.7")
        print(u"作者：Run Rain")
        print("-" * 25)
        self.session = requests.session()
        self.time = int(round(time.time() * 1000))  # 获取unix时间戳
        self.main_url = "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=" + str(self.time)
        self.key_url = "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time=" + str(
            self.time + 20100) + "&_=" + str(self.time + 20000)
        self.post_url = "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?time=" + str(self.time + 20050)
        # print self.main_url,self.key_url  # for test
        self.headers = {"Host": "jwxt.cumt.edu.cn",
                        "Connection": "keep-alive",
                        # "Content-Length":"470",
                        "Cache-Control": "max-age=0",
                        "Origin": "http://jwxt.cumt.edu.cn",
                        "Upgrade-Insecure-Requests": "1",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                        "Referer": "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=" + str(
                            self.time),
                        # "Accept-Encoding":"gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9"
                        }

    # 获取用户名和密码
    def get_user_info(self):
        if os.path.exists("user_info"):
            print(u"正在登录...")
            with open("user_info", "r") as f:
                info = f.read()
            self.num = base64.b64decode(info.split()[0])  # 用户信息解密
            self.password = base64.b64decode(info.split()[1])
        else:
            print(u"第一次登录初始化")
            print(u"请输入学号："),
            self.num = raw_input()
            # print(u"请输入密码："),
            self.password = getpass.getpass()  # 密码隐藏不显示
        self.get_captcha()

    # 获取验证码
    def get_captcha(self):
        captcha_url = "http://jwxt.cumt.edu.cn/jwglxt/kaptcha"
        try:
            captcha = self.session.get(captcha_url, headers=self.headers).content
        except Exception as e:
            print(u"连接失败，正在重连...")
            self.get_captcha()
        with open("captcha.jpeg", "wb") as f:
            f.write(captcha)
        os.startfile("captcha.jpeg")
        print(u"请输入验证码："),
        self.captcha = raw_input()
        self.get_csrftoken()

    # 获取csrftoken
    def get_csrftoken(self):
        response = self.session.get(self.main_url, headers=self.headers)
        html = response.text
        content = lxml.html.etree.HTML(html)
        self.csrftoken = content.xpath("//input[@id='csrftoken']/@value")[0]
        # print self.csrftoken  #for test
        self.get_publickey()

    # 获取加密公钥
    def get_publickey(self):
        response = self.session.get(self.key_url, headers=self.headers)
        key_data = response.json()
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]
        # print self.modulus,self.exponent  #for test
        self.get_RSA_password()

    # 获取RSA加密密码
    def get_RSA_password(self):
        rsa_key = RSAJS.RSAKey()
        rsa_key.setPublic(HB64().b642hex(self.modulus), HB64().b642hex(self.exponent))
        self.rsa_password = HB64().hex2b64(rsa_key.encrypt(self.password))
        # print self.rsa_password  #for test
        self.login()

    # 登录
    def login(self):
        self.data = {"csrftoken": self.csrftoken,
                     "yhm": self.num,
                     "mm": self.rsa_password,
                     "yzm": self.captcha
                     }
        headers = self.headers
        headers["Referer"] = "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html"
        response = self.session.post(self.post_url, data=self.data, headers=headers)
        if response.url == "http://jwxt.cumt.edu.cn/jwglxt/xtgl/index_initMenu.html":
            print(u"登录成功！")
            f = open("user_info", "w+")
            f.write(base64.b64encode(self.num))  # 用户信息加密后写入本地
            f.write("\n")
            f.write(base64.b64encode(self.password))
            f.close()
            self.user_info()
        else:
            print(u"用户名或密码或验证码不正确，请重试...")
            time.sleep(2)
            exit()

    def user_info(self):
        response = self.session.get(
            "http://jwxt.cumt.edu.cn/jwglxt/xtgl/index_cxYhxxIndex.html",
            headers=self.headers)
        # print response.text .encode('GBK','ignore').decode('GBk')  #for test
        try:
            html = response.text
            content = lxml.html.etree.HTML(html)
            self.name = content.xpath('//div[@class="media-body"]/h4/text()')[0]
            self.cls_str = content.xpath('//div[@class="media-body"]/p/text()')[0]
            self.college = self.cls_str.split()[0]
            self.cls = self.cls_str.split()[1]
            self.grade = str(re.findall('\d+', self.cls)[0])
            print(u"\n欢迎您，%s同学！\n" % self.name)
            print(u"=======个人信息=======")
            print(u"学号：%s" % self.num)
            print(u"姓名：%s" % self.name)
            print(u"学院：%s" % self.college)
            print(u"班级：%s" % self.cls)
            print(u"年级：%s" % self.grade)
            print("")
            time.sleep(1)
        except Exception as reason:
            response = self.session.get(
                "http://jwxt.cumt.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default",
                headers=self.headers)
            html = response.text
            content = lxml.html.etree.HTML(html)
            self.name = content.xpath('//div[@id="col_xm"]/p[@class="form-control-static"]/text()')[0]
            self.grade = content.xpath('//div[@id="col_rxrq"]/p[@class="form-control-static"]/text()')[0].split('-')[0]
            print(u"\n欢迎您，%s同学！\n" % self.name)
            print(u"=======个人信息=======")
            print(u"学号：%s" % self.num)
            print(u"姓名：%s" % self.name)
            print(u"年级：%s" % self.grade)
            print("")
        finally:
            self.activate(self.num, self.name)

    # 激活软件
    def activate(self, number, name):
        h = hashlib.md5()  # 创建md5对象
        s = number + name
        h.update(s.encode('utf-8'))
        CDKEY = "CDKEY_" + number  # 激活码文件名
        t = 0
        try:
            f = open(CDKEY, "r")
            text = f.read()
            if text.lower() == h.hexdigest():
                print(u"用户已激活！\n")
                f.close()
                t = 1
        except Exception as reason:
            while True:
                print(u"请输入激活码（请联系作者QQ：1121192423获取）："),
                text = raw_input()
                if text.lower() == h.hexdigest():
                    print(u"激活成功！\n")
                    with open(CDKEY, "w+") as f:
                        f.write(text)
                    time.sleep(1)
                    t = 1
                    break
                else:
                    print(u"激活码不正确，请重新输入")
        if t:
            FunctionMenu(self.session, self.num, self.name, self.grade)  # 调用功能


# 程序入口
if __name__ == "__main__":
    user = EducationalAdministrationSystem()
    user.get_user_info()
