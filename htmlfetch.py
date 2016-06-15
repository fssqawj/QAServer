# coding: utf8
import requests
from urllib import urlencode


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}


def fetch(url):
    r = requests.get(url, headers=header, timeout=100000)
    return r.text


if __name__ == '__main__':
    open('tem.txt', 'w').write(fetch('http://baike.baidu.com/search/none?word=刘诗诗的老公&enc=utf8'))
