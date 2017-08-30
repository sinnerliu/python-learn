# -*- coding:utf-8 -*-

import requests
import re
import os
from tqdm import trange

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


# 获取t66y最新地址
def getT66yUrl():
    url = 'http://get.xunfs.com/app/listapp.php'
    data = {}
    data["a"] = 'get'
    data["system"] = 'android'
    data["v"] = '1.5'
    get_url = requests.post(url, data=data, headers=headers).content.decode('UTF-8')
    re_url_all = re.compile(r'(http://[a-z.]+/)')
    t66y_url_all = re_url_all.findall(get_url)
    t66y_url = str(t66y_url_all[0])
    return t66y_url


# 获取页面
def getPage(url, pageNum):
    url = url + str(pageNum)
    page = requests.get(url, headers=headers)
    page.encoding = 'gbk'
    return page.text


# 获取页面数
def getPageNum(page):
    pattern = re.compile(
        r"table width=\"100%\" .*?onfocus=\"this.value='';\" onblur=\"this.value='1/(\d+)'\" onkeydown=\"javascript",
        re.S)
    pageNum = re.findall(pattern, page)[0]
    return int(pageNum)


# 获取指定页面中帖子的url
def getPageUrls(url, pageNum):
    page = getPage(url, pageNum)
    if pageNum == 1:
        pattern = re.compile(
            r'style="border-top:0">普通主題</td>(.*?)<table cellspacing="0" cellpadding="0" width="100%" align="center">',
            re.S)
        pageUrla = re.findall(pattern, page)
        patterna = re.compile(r'<h3><a href="(htm_data.*?)" target="_blank" id="">(.*?)</a></h3>', re.S)
        pageUrl = re.findall(patterna, pageUrla[0])
    else:
        pattern = re.compile(r'<h3><a href="(htm_data.*?)" target="_blank" id="">(.*?)</a></h3>', re.S)
        pageUrl = re.findall(pattern, page)
    pageUrls = []
    for item in pageUrl:
        pageUrls.append(item)
    return pageUrls


# 获取指定帖子中的图片url
def getPageImgUrl(url):
    url = t66yUrl + url
    page = getPage(url, '')
    pattern = re.compile(r"<input src='(.*?)' type='image' onclick=\"window.open", re.S)
    items = re.findall(pattern, page)
    return items


# 保存图片
def saveImg(url, num):
    imgName = str(num) + ".jpg"
    try:
        requests.packages.urllib3.disable_warnings()
        imgData = requests.get(url, headers=headers, verify=False)
        with open(imgName, 'wb') as img:
            img.write(imgData.content)
            img.close()
    except Exception as err:
        print(err)
        with open(pyPath+"/error.log", 'a') as errorlog:
            errorlog.write(url)
            errorlog.close()


# 创建文件夹
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print()


t66yUrl = getT66yUrl()
print(t66yUrl)
dagaierUrl = t66yUrl + 'thread0806.php?fid=16&search=&page='
pyPath = os.getcwd()
mkdir("data")
dataPath = pyPath + "/data"
os.chdir(dataPath)
page = getPage(dagaierUrl, 1)
pageNum = getPageNum(page)
for num in range(1, 101):
    # print(str(num)+"/100")
    pageUrls = getPageUrls(dagaierUrl, num)
    for pageOne in range(len(pageUrls)):
        path = pageUrls[pageOne][1].replace('<font color=green>', 'a').replace('</font>', '')
        mkdir(path)
        # print(path)
        os.chdir(path)
        imgUrls = getPageImgUrl(pageUrls[pageOne][0])
        for imgUrl in trange(len(imgUrls), desc=(str(num) + "-" + str(pageOne + 1))):
            saveImg(imgUrls[imgUrl], imgUrl)
        os.chdir(dataPath)
