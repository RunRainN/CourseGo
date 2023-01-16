# -*- coding:utf-8 -*-
import time
import os
from urllib import quote
import smtplib
from email.mime.text import MIMEText
from PublicElectiveCourse import PublicElectiveCourse


class FunctionMenu:
    def __init__(self, session, num, name, grade):
        self.session = session
        self.num = num
        self.name = name
        self.grade = grade
        self.headers = {"Host": "jwxt.cumt.edu.cn",
                        "Connection": "keep-alive",
                        # "Content-Length":"157",
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Origin": "http://jwxt.cumt.edu.cn",
                        "X-Requested-With": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                        # "Referer":"http://jwxt.cumt.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su=17184941",
                        # "Accept-Encoding":"gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9"
                        }
        self.menu()

    def menu(self):
        print(u"=======功能列表=======")
        print(u"1.成绩查询")
        print(u"2.课表查询")
        print(u"3.考试查询")
        print(u"4.公选课")
        print(u"5.报个Bug/提个建议")
        print(u"6.退出程序")
        # 用户输入判断
        while True:
            try:
                print(u"请选择相应功能的序号："),
                num = int(raw_input())
            except (ValueError, ZeroDivisionError):
                print(u"输入有误，请重新选择")
            else:
                if num < 1 or num > 6:
                    print(u"输入有误，请重新选择")
                else:
                    break
        if num == 1:
            self.exam_results()
        elif num == 2:
            self.schedule()
        elif num == 3:
            self.exam_info()
        elif num == 4:
            self.public_elective_course()
        elif num == 5:
            self.advice()
        elif num == 6:
            self.exit()

    # 功能1
    def exam_results(self):
        data = [("gnmkdmKey", "N305007"),
                ("sessionUserKey", str(self.num)),
                ("xnm", ""),
                ("xqm", ""),
                ("dcclbh", "JW_N305005_XSCXXMCJ"),
                ("queryModel.sortName", ""),
                ("queryModel.sortOrder", "asc"),
                ("exportModel.selectCol", "xnmmc%40%E5%AD%A6%E5%B9%B4"),
                ("exportModel.selectCol", "xqmmc%40%E5%AD%A6%E6%9C%9F"),
                ("exportModel.selectCol", "kkbmmc%40%E5%BC%80%E8%AF%BE%E5%AD%A6%E9%99%A2"),
                ("exportModel.selectCol", "kch%40%E8%AF%BE%E7%A8%8B%E4%BB%A3%E7%A0%81"),
                ("exportModel.selectCol", "kcmc%40%E8%AF%BE%E7%A8%8B%E5%90%8D%E7%A7%B0"),
                ("exportModel.selectCol", "jxbmc%40%E6%95%99%E5%AD%A6%E7%8F%AD"),
                ("exportModel.selectCol", "xf%40%E5%AD%A6%E5%88%86"),
                ("exportModel.selectCol", "xmblmc%40%E6%88%90%E7%BB%A9%E5%88%86%E9%A1%B9"),
                ("exportModel.selectCol", "xmcj%40%E6%88%90%E7%BB%A9"),
                ("exportModel.exportWjgs", "xls"),
                ("fileName", "exam_results")
                ]
        response = self.session.post("http://jwxt.cumt.edu.cn/jwglxt/cjcx/cjcx_dcXsKccjList.html", data=data,
                                     headers=self.headers)
        file_name = "exam_results" + str(int(time.time())) + ".xls"
        with open(file_name, "wb") as f:
            f.write(response.content)
        os.startfile(file_name)
        print(u'已将成绩"%s"保存至本地' % file_name)
        print(u"按回车键返回主菜单..."),
        raw_input()
        self.menu()

    # 功能2
    def schedule(self):
        xm = quote(quote(self.name.encode("utf-8")))  # 两次urlencode编码
        while True:
            try:
                print(u"请输入要查询的学期对应的总学期数：（例如：大二上则输入3，大三下则输入6）"),
                xqm = int(raw_input())
                break
            except (ValueError, ZeroDivisionError):
                print(u"输入有误，请重新输入")
        if xqm % 2:
            xnm = int(self.grade) + xqm / 2
            xqmmc = 1
            xnmc = str(xnm) + "-" + str(xnm + 1)
        else:
            xnm = int(self.grade) + xqm / 2 - 1
            xqmmc = 2
            xnmc = str(xnm) + "-" + str(xnm + 1)

        schedule_url = "http://jwxt.cumt.edu.cn/jwglxt/kbcx/xskbcx_cxXsShcPdf.html?doType=table&xszd.sj=true&xszd.cd=true&xszd.js=true&xszd.jszc=false&xszd.jxb=true&xszd.xkbz=true&xszd.kcxszc=true&xszd.zhxs=true&xszd.zxs=true&jgmc=undefined&xxdm=&gnmkdm=N2151&sessionUserKey=&xszd.xf=true" + "&xm=" + xm + "&xnm=" + str(
            xnm) + "&xqm=" + str(xqm) + "&xnmc=" + xnmc + "&xqmmc=" + str(xqmmc)
        response = self.session.get(schedule_url, headers=self.headers)
        file_name = "schedule" + "(" + str(xqm) + ")" + ".pdf"
        with open(file_name, "wb") as f:
            f.write(response.content)
        os.startfile(file_name)
        print(u'已将课表"schedule(%d).pdf"保存至本地' % xqm)
        print(u"按回车键返回主菜单..."),
        raw_input()
        self.menu()

    # 功能3
    def exam_info(self):
        data = [("gnmkdmKey", "N358105"),
                ("sessionUserKey", str(self.num)),
                ("xnm", ""),
                ("xqm", ""),
                ("ksmcdmb_id", ""),
                ("kch", ""),
                ("kc", ""),
                ("ksrq", ""),
                ("dcclbh", "JW_N358105_KSCX"),
                ("queryModel.sortName", ""),
                ("queryModel.sortOrder", "asc"),
                ("exportModel.selectCol", "xnmc%40%E5%AD%A6%E5%B9%B4"),
                ("exportModel.selectCol", "xqmmc%40%E5%AD%A6%E6%9C%9F"),
                ("exportModel.selectCol", "xh%40%E5%AD%A6%E5%8F%B7"),
                ("exportModel.selectCol", "xm%40%E5%A7%93%E5%90%8D"),
                ("exportModel.selectCol", "xb%40%E6%80%A7%E5%88%AB"),
                ("exportModel.selectCol", "bj%40%E7%8F%AD%E7%BA%A7"),
                ("exportModel.selectCol", "kch%40%E8%AF%BE%E7%A8%8B%E4%BB%A3%E7%A0%81"),
                ("exportModel.selectCol", "kcmc%40%E8%AF%BE%E7%A8%8B%E5%90%8D%E7%A7%B0"),
                ("exportModel.selectCol", "jsxx%40%E6%95%99%E5%B8%88%E4%BF%A1%E6%81%AF"),
                ("exportModel.selectCol", "cxbj%40%E9%87%8D%E4%BF%AE%E6%A0%87%E8%AE%B0"),
                ("exportModel.selectCol", "zxbj%40%E8%87%AA%E4%BF%AE%E6%A0%87%E8%AE%B0"),
                ("exportModel.selectCol", "ksmc%40%E8%80%83%E8%AF%95%E5%90%8D%E7%A7%B0"),
                ("exportModel.selectCol", "sjbh%40%E8%AF%95%E5%8D%B7%E7%BC%96%E5%8F%B7"),
                ("exportModel.selectCol", "kssj%40%E8%80%83%E8%AF%95%E6%97%B6%E9%97%B4"),
                ("exportModel.selectCol", "cdmc%40%E8%80%83%E8%AF%95%E5%9C%B0%E7%82%B9"),
                ("exportModel.selectCol", "cdxqmc%40%E8%80%83%E8%AF%95%E6%A0%A1%E5%8C%BA"),
                ("exportModel.selectCol", "ksbz%40%E8%80%83%E8%AF%95%E5%A4%87%E6%B3%A8"),
                ("exportModel.selectCol", "jxbmc%40%E6%95%99%E5%AD%A6%E7%8F%AD%E5%90%8D%E7%A7%B0"),
                ("exportModel.selectCol", "jxbzc%40%E6%95%99%E5%AD%A6%E7%8F%AD%E7%BB%84%E6%88%90"),
                ("exportModel.selectCol", "xqmc%40%E6%A0%A1%E5%8C%BA%E5%90%8D%E7%A7%B0"),
                ("exportModel.selectCol", "sksj%40%E4%B8%8A%E8%AF%BE%E6%97%B6%E9%97%B4"),
                ("exportModel.selectCol", "jxdd%40%E4%B8%8A%E8%AF%BE%E5%9C%B0%E7%82%B9"),
                ("exportModel.selectCol", "njmc%40%E5%B9%B4%E7%BA%A7"),
                ("exportModel.selectCol", "jgmc%40%E5%AD%A6%E9%99%A2"),
                ("exportModel.selectCol", "zymc%40%E4%B8%93%E4%B8%9A"),
                ("exportModel.exportWjgs", "xls"),
                ("fileName", "exam_info")
                ]
        response = self.session.post("http://jwxt.cumt.edu.cn/jwglxt/kwgl/kscx_dcXsksxxList.html", data=data,
                                     headers=self.headers)
        file_name = "exam_info" + str(int(time.time())) + ".xls"
        with open(file_name, "wb") as f:
            f.write(response.content)
        os.startfile(file_name)
        print(u'已将考试信息"%s"保存至本地' % file_name)
        print(u"按回车键返回主菜单..."),
        raw_input()
        self.menu()

    # 功能4
    def public_elective_course(self):
        PublicElectiveCourse(self.session)
        print(u"按回车键返回主菜单..."),
        raw_input()
        self.menu()

    # 功能5
    def advice(self):
        msg_from = "1121192423@qq.com"  # 发送方邮箱
        passwd = "ltorahvoyrovgjif"  # 发送方邮箱的授权码
        msg_to = "1121192423@qq.com"  # 收件人邮箱

        subject = "EducationalAdministrationSystem_advice"  # 主题
        print(u"请输入Bug或建议："),
        content = raw_input()  # 正文
        print(u"请输入您的联系方式（例如QQ，输入为空则匿名发送）："),
        info = raw_input()
        subject += info
        msg = MIMEText(content)
        msg["Subject"] = subject
        msg["From"] = msg_from
        msg["To"] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print(u"发送成功！感谢您的建议")
        except Exception as e:
            print(u"发送失败...")
        finally:
            s.quit()
            print(u"按回车键返回主菜单..."),
            raw_input()
            self.menu()

    # 功能6
    def exit(self):
        print(u"谢谢使用！")
        time.sleep(1)
        exit()
