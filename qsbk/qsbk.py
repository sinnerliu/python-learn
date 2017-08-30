# -*- coding:utf-8 -*-

import requests
import re
import os
import time
from tqdm import tqdm

base_url="https://www.qiushibaike.com"
pageUrl='https://www.qiushibaike.com/text/page/'
headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Host":"www.qiushibaike.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}
def getPage(page):
    url=pageUrl+str(page)
    req=requests.get(url,headers=headers,timeout=3).text
    # print(req)
    pattern=re.compile(r'<div class="articleGender \w+Icon">\d+</div>.*?</div>.*?<a href="(.*?)" target="_blank" class="contentHerf" onclick="_hmt.push',re.S)
    urls=re.findall(pattern,req)
    return urls

def getText(url):
    url=base_url+url
    req=requests.get(url,headers=headers,timeout=3).text
    pattern=re.compile(r'target="_blank" title="(.*?)">.*?content">(.*?)</div>.*?number">(\d+)</i>.*?number">(\d+)</i>',re.S)
    contents=re.findall(pattern,req)
    for i in contents:
        pattern='<br/><br/>|<br/>'
        content=re.sub(pattern,'',i[1].strip())
        text="###发布人:"+i[0].strip()+" 好笑:"+i[2]+" 评论:"+i[3]+" 地址:"+url+"\r\n"+content+"\r\n\r\n"
        # print(text)
        text.encode('utf-8')
        writeText(text)

def fileExists(filename):
    if os.path.exists(filename):
        print("filename:"+filename)
        os.remove(filename)
    else:
        print("filename:"+filename)

def writeText(text):
    with open(filename,'a',encoding='utf-8') as txt:
        txt.write(text)
        txt.close()

filename="qsbk.txt"
fileExists(filename)
for i in range(1,10):
    urls=getPage(i)
    for url in tqdm(urls,desc='Page '+str(i)):
        time.sleep(3)
        getText(url)
