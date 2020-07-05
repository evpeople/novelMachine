import requests
import re
from bs4 import BeautifulSoup
import time


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
    
    if title.find(u"有一") != -1:
        f = open("wyyzkbw.txt","w")
        f.write(title+"\n\n"+guo)        
        f.close
    elif title.find(u"师兄") != -1:
        f = open("wsxsz.txt","w")
        f.write(title+"\n\n"+guo)
        f.close
    elif title.find(u"复苏") != -1:
        f = open("kbfs.txt","w")
        f.write(title+"\n\n"+guo) 
        f.close
    elif title.find(u"首富") != -1:
        f = open("kcsf.txt","w")
        f.write(title+"\n\n"+guo) 
        f.close
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
    CatLogy = CatLogy.encode("ISO-8859-1")
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

web = {'kbw':'http://www.biqu6.com/23_23554/','wsx':'http://www.biqu6.com/49_49868/','kbf':'http://www.biqu6.com/25_25220/','ksf':'http://www.biqu6.com/48_48213/'}

for x in web.values():
    time.sleep(20)
    h=getCatlogy(x)
    if h==0:
        print("没更新\n")
        continue
    else:
        getOnePage(h)


