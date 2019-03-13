import requests
from bs4 import BeautifulSoup             # 从bs4这个库中导入BeautifulSoup

link = "http://www.santostang.com/"
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/71.0.3578.98'}
resp = requests.get(link, headers = headers)

soup = BeautifulSoup(resp.text, "lxml")   # 使用BeautifulSoup解析这段代码
title = soup.find("h1", class_ = "post-title").a.text.strip()

def getText():
    pass

def getUrl():
    pass

def getImage():
    pass

def saveImage():
    pass


if __name__ == "__main__":
    base_url = 'www.yaoyaomanhua.wang/html/_toukui_di2ji/2018/0723/'
    temp_url = '1389.html'
    image_url = 'http://www.yaoyaomanhua.wang/uploads/allimg/180723/1-1PH31F537.jpg'
