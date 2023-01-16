# -*- coding:utf-8 -*-

import hashlib

h = hashlib.md5()  # 创建md5对象
s = u"12345678张三"
h.update(s.encode('utf-8'))
print(h.hexdigest().upper())
