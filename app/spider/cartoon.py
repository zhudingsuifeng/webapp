#coding = utf-8

import os
import re
import requests
import urllib.request
from bs4 import BeautifulSoup
import time

# 将对应url图片保存到本地
def getImg(imgUrl, chapter, name):
    path = os.path.join('/home/fly/git/webapp/app/static/imgs', str(chapter))
    if not os.path.exists(path):    # 判断文件夹是否存在，不存在则创建
        os.mkdir(path)
    imgName = str(name) + '.jpg'
    imgName = os.path.join(path, imgName)
    urllib.request.urlretrieve(imgUrl, imgName)
    print("download " + str(name) + " to computer")

# 获取单个章节中所有图片的url
def getImgUrl(url, headers, chapter):
    resp = requests.get(url, headers = headers)
    soup = BeautifulSoup(resp.text, 'lxml')    # 使用BeautifulSoup解析这段代码
    links = soup.select("img")
    image_url = 'http://www.yaoyaomanhua.wang'
    name = 1
    for link in links:
        time.sleep(1)
        img = link.get("src")
        getImg(image_url+img, chapter, name)
        name += 1

# 开始爬去，获取所有章节的对应url
def getStart(url, headers):
    resp = requests.get(url, headers = headers)
    soup = BeautifulSoup(resp.text, 'lxml')    # 使用BeautifulSoup解析这段代码
    contexts = soup.find_all(href = re.compile("_toukui_di2ji"))   # 寻找标签中超链接里面带有相关字符的标签，以列表的形式返回
    chapter = 1
    # 总共71话
    for item in contexts[::-1]:
        url = 'http://www.yaoyaomanhua.wang'+item.get('href')
        getImgUrl(url, headers, chapter)
        print("-----------第 " + str(chapter) + " 话下载完成-------------")
        chapter += 1
        time.sleep(6)
        # break

if __name__ == "__main__":
    url = 'http://www.yaoyaomanhua.wang/html/_toukui_di2ji/'
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/71.0.3578.98'}
    getStart(url, headers)