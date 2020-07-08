#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr







# 下面的url是待抓取的小说页面，也就是传入的参数
url = "http://www.biqu6.com/23_23554/27344021.html"
response = requests.get(url)
wenzhang = response.text
wenzhang=wenzhang.encode("ISO-8859-1")
wenzhang=wenzhang.decode("utf-8")
#上面在抓取并解码，下面是形成一个满足beautifulsoup的变量
cheng = BeautifulSoup(wenzhang,'html.parser')
#寻找小说内容
guo = cheng.find('div',id='content')

guo=str(guo)
p = r'<div id="content">'
guo=re.sub("<br/>","\n",guo)
guo=re.sub(p," ",guo)
guo=re.sub("</div>","",guo)
#洗小说内容
title = cheng.find('title')
title=str(title)
title=re.sub("<title>"," ",title)
title=re.sub("</title>"," ",title)
title=re.sub("新笔趣阁","",title)
title=re.sub("正文卷","",title)
#洗标题


msg=MIMEText(title+"\n\n"+guo,'plain','utf-8')
msg['From']=formataddr(["FromRunoob",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
msg['Subject']="测试"
server=smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
server.login(my_sender, my_pass)
server.sendmail(my_sender,[my_user,],msg.as_string())
server.quit()


if title.find(u"有一") != -1:
    f = open("wyyzkbw.txt","w")
    f.write(title+"\n\n"+guo)
    f.close


