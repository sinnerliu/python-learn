# -*- coding:utf-8 -*-

import requests
import re
import os
import asyncio


page='1'


if  os.path.exists('data'):
    print()
else:
    try:
        os.mkdir('data')
    except   FileExistsError as e:
        print(e)

os.chdir('data')
py_path = os.getcwd()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


def get_form_url():
    url_html = requests.get('http://caregirl.net/hkpic.html', headers=headers).content.decode('UTF-8')
    re_url_html = re.compile(r'(http://.*)<br><br>')
    form_url = re_url_html.findall(url_html)
    form_urla = str(form_url[0]) + "/"
    return form_urla


base_url = get_form_url()
print("论坛最新地址为:" + base_url)
login_url = base_url + 'member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'

thumb = '.thumb.jpg'
# thumb=''


data = {}
data["fastloginfield"] = "username"
data["username"] = "284716337"
data["password"] = "bisi284716"
data["quickforward"] = "yes"
data["handlekey"] = "ls"


async def download_jpg(base_url,url,headers,thumb):
    jpg_url=url
    print(jpg_url)
    img_name=jpg_url.split('/')[-1].split('.')[0]
    print(img_name)
    image = requests.get(base_url + jpg_url + thumb, stream=True, headers=headers)
    with open(str(img_name) + ".jpg" + thumb, 'wb') as jpg:
        jpg.write(image.content)
        jpg.close()


# proxies = {"http": "http://127.0.0.1:1086", }

session = requests.Session()
session.headers = headers

login = session.post(login_url, data=data, headers=headers)
forum_url = base_url + 'forum.php?mod=forumdisplay&fid=18&orderby=dateline&filter=author&orderby=dateline&page='+page
forum_text = session.get(forum_url, headers=headers).content.decode('UTF-8')
# re_url = re.compile(r'href="(thread-\d+-\d+-\d+.html)"  onclick="atarget\(this\)" title="(.*)" class="z">')
re_url = re.compile(r'href="(forum.php\?mod=viewthread&amp;tid=\d+&amp;extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26orderby%3Ddateline)"  onclick="atarget\(this\)" title="(.*)" class="z">')
AllUrl = re_url.findall(forum_text)
for i in AllUrl:
    # print(i[1],":"+i[0])
    if os.path.exists(i[1]):
        print(i[1]+'is exists')
    else:
        try:
            os.mkdir(i[1])
            print(i[1])
        except   FileExistsError as e:
            print(e)
        os.chdir(i[1])
        forum_text_one = session.get(base_url + i[0].replace('amp;', ''), headers=headers).content.decode('UTF-8')
        re_jpg_url = re.compile(r'zoomfile="(data/attachment/forum/\d{6}/\d{1,2}/[0-9a-zA-Z]+.jpg)"')
        jpg_urls = re_jpg_url.findall(forum_text_one)
        img_name = 1
        #协程
        loop = asyncio.get_event_loop()
        tasks = [download_jpg(base_url,url,headers,thumb) for url in jpg_urls]
        loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()
        # for jpg_url in jpg_urls:
        #     # print(jpg_url)
        #     print(img_name)
        #     image = requests.get(base_url + jpg_url + thumb, stream=True, headers=headers)
        #     with open(str(img_name) + ".jpg" + thumb, 'wb') as jpg:
        #        jpg.write(image.content)
        #        jpg.close()

            # img_name = img_name + 1
        print(i[1]+":" +str(img_name)+"P" )
        os.chdir(py_path)
