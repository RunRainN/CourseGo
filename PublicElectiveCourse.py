# -*- coding:utf-8 -*-

import re
import time


class PublicElectiveCourse:
    def __init__(self, session):
        self.session = session
        self.headers = {"Host": "jwxt.cumt.edu.cn",
                        "Connection": "keep-alive",
                        "Cache-Control": "max-age=0",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                        # "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9"
                        }
        while True:
            try:
                response = self.session.get(
                    "http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default",
                    headers=self.headers)
                break
            except:
                print(u"连接失败，正在重试")
        try:
            html = response.text  # 获取四个模块post需要的相同data参数
            self.xslbdm = re.compile('<input type="hidden" name="xslbdm" id="xslbdm" value="(.*)"/>').findall(html)[0]
            self.zyfx_id = re.compile('<input type="hidden" name="zyfx_id" id="zyfx_id" value="(.*)"/>').findall(html)[0]
            self.bh_id = re.compile('<input type="hidden" name="bh_id" id="bh_id" value="(.*)"/>').findall(html)[0]
            self.xsbj = re.compile('<input type="hidden" name="xsbj" id="xsbj" value="(.*)"/>').findall(html)[0]
            self.ccdm = re.compile('<input type="hidden" name="ccdm" id="ccdm" value="(.*)"/>').findall(html)[0]
            self.xkxqm = re.compile('<input type="hidden" name="xkxqm" id="xkxqm" value="(.*)"/>').findall(html)[0]
            self.xkxnm = re.compile('<input type="hidden" name="xkxnm" id="xkxnm" value="(.*)"/>').findall(html)[0]
            self.njdm_id = re.compile('<input type="hidden" name="njdm_id" id="njdm_id" value="(.*)"/>').findall(html)[0]
            self.xqh_id = re.compile('<input type="hidden" name="xqh_id" id="xqh_id" value="(.*)"/>').findall(html)[0]
            self.zyh_id = re.compile('<input type="hidden" name="zyh_id" id="zyh_id" value="(.*)"/>').findall(html)[0]
            self.jg_id = re.compile('<input type="hidden" name="jg_id_1" id="jg_id_1" value="(.*)"/>').findall(html)[0]
            self.xbm = re.compile('<input type="hidden" name="xbm" id="xbm" value="(.*)"/>').findall(html)[0]
            self.jxbzb = re.compile('<input type="hidden" name="jxbzb" id="jxbzb" value="(.*)"/>').findall(html)[0]
            self.xkkz_id = \
                re.compile('<input type="hidden" name="firstXkkzId" id="firstXkkzId" value="(.*)"/>').findall(html)[0]
            modules = re.compile('queryCourse(.*)</a></li>').findall(html)
        except:
            print(u"加载失败，选课系统可能未开放")
            return
        print(u"当前开放可选模块：")
        for text in modules:
            print text
        while True:
            print(u"[A/B/C]（A:继续\tB:刷新\tC:返回主菜单）："),
            judge = raw_input()
            if judge.upper() == "A":
                print(u"请输入选择模块对应的编号："),
                self.kklxdm = raw_input()
                print(u"请输入选择模块对应的字符串："),
                self.xkkz_id = raw_input()
                print(u"请输入要查询的课程代码（字母需大写）："),
                self.filter_list = raw_input()
                break
            elif judge.upper() == "B":
                self.__init__(self.session)
                return
            elif judge.upper() == "C":
                return
            else:
                print(u"输入有误，请重新输入")
        while True:
            try:
                response = self.session.post(
                    "http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbDisplay.html?gnmkdm=N253512",
                    headers=self.headers, data={"xkkz_id": self.xkkz_id, "xszxzt": "1", "kspage": 0, "jspage": "0"})
                break
            except:
                print(u"连接失败，正在重试")
        html = response.text  # 获取四个模块post需要的相同data参数
        self.sfkgbcx = re.compile('<input type="hidden" name="sfkgbcx" id="sfkgbcx" value="(.*)"/>').findall(html)[0]
        self.kkbkdj = re.compile('<input type="hidden" name="kkbkdj" id="kkbkdj" value="(.*)"/>').findall(html)[0]
        self.rlkz = re.compile('<input type="hidden" name="rlkz" id="rlkz" value="(.*)"/>').findall(html)[0]
        self.sfznkx = re.compile('<input type="hidden" name="sfznkx" id="sfznkx" value="(.*)"/>').findall(html)[0]
        self.tykczgxdcs = \
            re.compile('<input type="hidden" name="tykczgxdcs" id="tykczgxdcs" value="(.*)"/>').findall(html)[0]
        self.sfrxtgkcxd = \
            re.compile('<input type="hidden" name="sfrxtgkcxd" id="sfrxtgkcxd" value="(.*)"/>').findall(html)[0]
        self.sfkcfx = re.compile('<input type="hidden" name="sfkcfx" id="sfkcfx" value="(.*)"/>').findall(html)[0]
        self.zdkxms = re.compile('<input type="hidden" name="zdkxms" id="zdkxms" value="(.*)"/>').findall(html)[0]
        self.sfkxq = re.compile('<input type="hidden" name="sfkxq" id="sfkxq" value="(.*)"/>').findall(html)[0]
        self.sfkknj = re.compile('<input type="hidden" name="sfkknj" id="sfkknj" value="(.*)"/>').findall(html)[0]
        self.cxbj = "0"
        self.fxbj = "0"
        self.xkly = re.compile('<input type="hidden" name="xkly" id="xkly" value="(.*)"/>').findall(html)[0]
        self.sfkkzy = re.compile('<input type="hidden" name="sfkkzy" id="sfkkzy" value="(.*)"/>').findall(html)[0]
        self.kspage = "1"
        self.jspage = "10"
        data = [("xkkz_id", self.xkkz_id),
                ("xszxzt", "1"),
                ("kspage", "0"),
                ("jspage", "0")
                ]
        while True:
            try:
                res = self.session.post(
                    "http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbDisplay.html?gnmkdm=N253512", data=data,
                    headers=self.headers)
                break
            except:
                print(u"连接失败，正在重试")
        html0 = res.text  # 获取四个模块post需要的不同data参数
        self.rwlx = re.compile('<input type="hidden" name="rwlx" id="rwlx" value="(.*)"/>').findall(html0)[0]
        self.bklx_id = re.compile('<input type="hidden" name="bklx_id" id="bklx_id" value="(.*)"/>').findall(
            html0)[0]
        self.kkbk = re.compile('<input type="hidden" name="kkbk" id="kkbk" value="(.*)"/>').findall(html0)[0]
        self.search()

    def search(self):
        data_item = [("filter_list[0]", self.filter_list),
                     ("rwlx", self.rwlx),
                     ("xkly", self.xkly),
                     ("bklx_id", self.bklx_id),
                     ("xqh_id", self.xqh_id),
                     ("jg_id", self.jg_id),
                     ("zyh_id", self.zyh_id),
                     ("zyfx_id", self.zyfx_id),
                     ("njdm_id", self.njdm_id),
                     ("bh_id", self.bh_id),
                     ("xbm", self.xbm),
                     ("xslbdm", self.xslbdm),
                     ("ccdm", self.ccdm),
                     ("xsbj", self.xsbj),
                     ("sfkknj", self.sfkknj),
                     ("sfkkzy", self.sfkkzy),
                     ("sfznkx", self.sfznkx),
                     ("zdkxms", self.zdkxms),
                     ("sfkxq", self.sfkxq),
                     ("sfkcfx", self.sfkcfx),
                     ("kkbk", self.kkbk),
                     ("kkbkdj", self.kkbkdj),
                     ("sfkgbcx", self.sfkgbcx),
                     ("sfrxtgkcxd", self.sfrxtgkcxd),
                     ("tykczgxdcs", self.tykczgxdcs),
                     ("xkxnm", self.xkxnm),
                     ("xkxqm", self.xkxqm),
                     ("kklxdm", self.kklxdm),
                     ("rlkz", self.rlkz),
                     ("kspage", self.kspage),
                     ("jspage", self.jspage),
                     ("jxbzb", self.jxbzb)
                     ]
        while True:
            try:
                response_item = self.session.post(
                    "http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512",
                    data=data_item,
                    headers=self.headers)
                break
            except:
                print(u"连接失败，正在重试")

        html1 = response_item.text
        try:
            self.kch_id = re.compile('"kch_id":"(.*?)"').search(html1).group(1)
        except Exception as e:
            print(u"输入有误，查询失败，请重试...")
            time.sleep(1)
            self.__init__(self.session)
        data_teacher = [("filter_list[0]", self.filter_list),
                        ("rwlx", self.rwlx),
                        ("xkly", self.xkly),
                        ("bklx_id", self.bklx_id),
                        ("xqh_id", self.xqh_id),
                        ("jg_id", self.jg_id),
                        ("zyh_id", self.zyh_id),
                        ("zyfx_id", self.zyfx_id),
                        ("njdm_id", self.njdm_id),
                        ("bh_id", self.bh_id),
                        ("xbm", self.xbm),
                        ("xslbdm", self.xslbdm),
                        ("ccdm", self.ccdm),
                        ("xsbj", self.xsbj),
                        ("sfkknj", self.sfkknj),
                        ("sfkkzy", self.sfkkzy),
                        ("sfznkx", self.sfznkx),
                        ("zdkxms", self.zdkxms),
                        ("sfkxq", self.sfkxq),
                        ("sfkcfx", self.sfkcfx),
                        ("kkbk", self.kkbk),
                        ("kkbkdj", self.kkbkdj),
                        ("xkxnm", self.xkxnm),
                        ("xkxqm", self.xkxqm),
                        ("rlkz", self.rlkz),
                        ("kklxdm", self.kklxdm),
                        ("kch_id", self.kch_id),
                        ("cxbj", self.cxbj),
                        ("fxbj", self.fxbj),
                        ("xkkz_id", self.xkkz_id)
                        ]
        while True:
            try:
                response_teacher = self.session.post(
                    "http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512",
                    data=data_teacher,
                    headers=self.headers)
                break
            except:
                print(u"连接失败，正在重试")
        html2 = response_teacher.text
        name_list = re.compile('"kcmc":"(.*?)"').findall(html1)
        teacher_list = re.compile('"jsxx":"(.*?)"').findall(html2)
        time_list = re.compile('"sksj":"(.*?)"').findall(html2)
        place_list = re.compile('"jxdd":"(.*?)"').findall(html2)
        selected_list = re.compile('"yxzrs":"(.*?)"').findall(html1)
        total_list = re.compile('"jxbrl":"(.*?)"').findall(html2)
        jxb_id_list = re.compile('"do_jxb_id":"(.*?)"').findall(html2)  # jwb_id(html1) or do_jxb_id(html2)
        number = len(teacher_list)
        print("%s%20s%30s%70s%50s%30s" % (u"序号", u"课程名", u"教师", u"时间", u"地点", u"已选\容量"))
        choose_dict = {}
        try:
            for i in range(number):
                print('-' * 200)
                print(
                    "%d%20s%30s%70s%50s%20s/%s" % (
                        i + 1, name_list[i], teacher_list[i], time_list[i],
                        place_list[i], selected_list[i], total_list[i]))
                choose_dict.update({str(i + 1): jxb_id_list[i]})
        except Exception as e:
            print(u"无可选课程")
        while True:
            print(u"[A/B]（A:继续\tB:返回主菜单）："),
            judge = raw_input()
            if judge.upper() == "A":
                self.choose(number, choose_dict)
                return
            elif judge.upper() == "B":
                return
            else:
                print(u"输入有误，请重新输入")

    def choose(self, number, choose_dict):
        while True:
            try:
                print(u"请选择序号："),
                num = int(raw_input())
            except (ValueError, ZeroDivisionError):
                print(u"输入有误，请重新选择")
            else:
                if num < 1 or num > number:
                    print(u"输入有误，请重新选择")
                else:
                    break
        data = [("kcmc", ""),
                ("rlkz", self.rlkz),
                ("qz", "0"),
                ("cxbj", self.cxbj),
                ("xxkbj", "0"),
                ("kklxdm", self.kklxdm),
                ("rwlx", self.rwlx),
                ("rlzlkz", "1"),
                ("xklc", "1"),
                ("sxbj", "1"),
                ("zyh_id", self.zyh_id),
                ("njdm_id", self.njdm_id),
                ("xkxnm", self.xkxnm),
                ("xkxqm", self.xkxqm),
                ("jxb_ids", choose_dict[str(num)]),
                ("xkkz_id", self.xkkz_id),
                ("kch_id", self.kch_id)
                ]
        i = 1
        while True:
            print(u"正在进行第%d次尝试，当前系统时间：%s" % (i, time.ctime()))
            while True:
                try:
                    response = self.session.post(
                        "http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512",
                        data=data, headers=self.headers)
                    break
                except:
                    print(u"连接失败，正在重试")
            print response.text
            if eval(response.content)["flag"] == "1":
                print(u"选课成功！")
                break
            elif eval(response.content)["flag"] == "0":
                print(u"该门课已选教学班或时间冲突！")
            elif eval(response.content)["flag"] == "-1":
                print(u"人数已满！")
            print('-' * 50)
            time.sleep(1)  # 为服务器着想，适合夜间捡漏
            i += 1
        '''
            if i % 100 == 0:
                while True:
                    print(u"[A/B]（A:继续\tB:返回）："),
                    judge = raw_input()
                    if judge.upper() == "A":
                        break
                    elif judge.upper() == "B":
                        return
                    else:
                        print(u"输入有误，请重新输入")
        '''
