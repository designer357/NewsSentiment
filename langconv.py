# -*- coding:utf-8 -*-
from zhtools.langconv import *
line = "萬達"
line=line.decode("utf-8")
print(line)
#转换繁体到简体
line = Converter('zh-hans').convert(line)
line = line.encode('utf-8')
print(line)
# 转换简体到繁体
#line = Converter('zh-hant').convert(line.decode('utf-8'))
#line = line.encode('utf-8')