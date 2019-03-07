#!/usr/bin/env python
#coding=utf-8
#python3.6.5

import urllib.request
import re,sys

def get_html(url):
    html=urllib.request.urlopen(url).read()
    return html

def get_url_name(html):
    html=html.decode("utf-8")
    #rname=re.compile(r'<img alt=".*?" src')  #'<img alt="欢度国庆" src'
    rname=re.compile(r'<img alt="(.*?)" src') #'欢度国庆'
    names=re.findall(rname,html)
    rurl=re.compile(r'<img alt=".*?" src="(.*?)" data-reactid')
    urls=re.findall(rurl,html)
    return names,urls

def download(url,name):
    path=r'imgs/%s.jpg' % name
    url=r'https:%s' % url
    urllib.request.urlretrieve(url,path) #python3 urllib.request.urlretrieve() get remote data to local

def mongo(url,name):
    return 0

if __name__=="__main__":
    html=get_html("https://xiaba.shijue.me/photo")
    names,urls=get_url_name(html)
    for name,url in zip(names,urls):
        download(url,name)
        print(name+" success")
