#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import os
from apscheduler.schedulers.blocking import BlockingScheduler

def getOnePage(url):

    # 下面的url是待抓取的小说页面，也就是传入的参数
    #url = "http://www.biqu6.com/23_23554/27344021.html"
    response = requests.get(url)
    wenzhang = response.text
    wenzhang = wenzhang.encode("ISO-8859-1")
    wenzhang = wenzhang.decode("utf-8")
    #上面在抓取并解码，下面是形成一个满足beautifulsoup的变量
    cheng = BeautifulSoup(wenzhang, 'html.parser')
    #寻找小说内容
    guo = cheng.find('div', id='content')

    guo = str(guo)
    p = r'<div id="content">'
    guo = re.sub("<br/>", "\n", guo)
    guo = re.sub(p, " ", guo)
    guo = re.sub("</div>", "", guo)
    #洗小说内容
    title = cheng.find('title')
    title = str(title)
    title = re.sub("<title>", " ", title)
    title = re.sub("</title>", " ", title)
    title = re.sub("新笔趣阁", "", title)
    title = re.sub("正文卷", "", title)
    #洗标题

    hf=open("temp.txt","w+")
    hf.write(guo)
    

    msg=MIMEText(title+"\n\n"+guo,'plain','utf-8')
    msg['From']=formataddr(["小说机",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject']=title
    server=smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender,[my_user,],msg.as_string())
    server.quit()

def getCatlogy(url):
    #下面为带传入的参数
    #url = "http://www.biqu6.com/23_23554/"

    url1 = "http://www.biqu6.com/23_23554/"
    url2 = "http://www.biqu6.com/49_49868/"
    url3 = "http://www.biqu6.com/25_25220/"
    url4 = "http://www.biqu6.com/48_48213/"

    if url1==url:
        d="kbw.txt"
    elif url2==url:
        d="wsx.txt"
    elif url3==url:
        d="kbf.txt"
    elif url4==url:
        d="ksf.txt"    
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
        return 0
    else:
        p=r"<meta property="
        q=r'"og:novel:latest_chapter_url"'
        linex = re.sub(p,"",linex)
        linex = re.sub(q,"",linex)
        linex = re.sub("content=","",linex)
        linex = re.sub("/>","",linex)
        linex = re.sub('"',"",linex)
        #更改了则进行抓取
        return linex

def tick():
    web = {'kbw':'http://www.biqu6.com/23_23554/','wsx':'http://www.biqu6.com/49_49868/','kbf':'http://www.biqu6.com/25_25220/','ksf':'http://www.biqu6.com/48_48213/'}

    for x in web.values():
        time.sleep(5)
        h=getCatlogy(x)
        if h==0:
            fil=open("logg.txt","a+")
            localtime = time.asctime( time.localtime(time.time()) )
            str(localtime)
            fil.write("没更新  \n"+localtime)
            fil.close
            continue
        else:
            getOnePage(h)
    fil.write("\n")


sched = BlockingScheduler()
sched.add_job(tick, 'interval', seconds=900)
sched.start()
