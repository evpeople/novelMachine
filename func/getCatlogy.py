#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
#下面为带传入的参数
url1 = "http://www.biqu6.com/23_23554/"
url = "http://www.biqu6.com/49_49868/"
url3 = "http://www.biqu6.com/25_25220/"
url4 = "http://www.biqu6.com/48_48213/"

d="kbf.txt"

response = requests.get(url)
CatLogy = response.text
CatLogy = CatLogy.encode("utf-8")
CatLogy = CatLogy.decode("utf-8")


#需要if判断，来增加小说，可重构
with open(d, "r") as f:
    i = 1
    while i < 22:
        line = f.readline()
        i = i+1
f.close
# print(line)
#上面在读原本的目录页的最新章节
ca = open(d, "w")
ca.write(CatLogy)
ca.close
# 写入新目录页
with open(d, "r") as f:
    i = 1
    while i < 22:
        linex = f.readline()
        i = i+1
f.close
#读取新目录页的第21行是不是更改了
if line == linex:
    flag = 1
else:
    p=r"<meta property="
    q=r'"og:novel:latest_chapter_url"'
    linex = re.sub(p,"",linex)
    linex = re.sub(q,"",linex)
    linex = re.sub("content=","",linex)
    linex = re.sub("/>","",linex)
    linex = re.sub('"',"",linex)
    #更改了则进行抓取
